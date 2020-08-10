import argparse
import ast
import codecs
import functools
import operator
import os
import re
import shutil
import string
import sys

from django.apps import apps

# from default.settings import BASE_DIR

BASE_TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
VIEW_CLASSES = [
    "List",
    "Create",
    "Detail",
    "Update",
    "Delete"
]


def convert(name):
    """
    This function converts a Camel Case word to a underscore word
    """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def render_template_with_args_in_file(file, template_file_name, **kwargs):
    """
    Get a file and render the content of the template_file_name with kwargs in a file
    :param file: A File Stream to write
    :param template_file_name: path to route with template name
    :param **kwargs: Args to be rendered in template
    """
    template_file_content = "".join(
        codecs.open(
            template_file_name,
            encoding='UTF-8'
        ).readlines()
    )
    template_rendered = string.Template(template_file_content).safe_substitute(**kwargs)
    file.write(template_rendered)


def create_or_open(file_name, initial_template_file_name, args):
    """
    Creates a file or open the file with file_name name
    :param file_name: String with a filename
    :param initial_template_file_name: String with path to initial template
    :param args: from console to determine path to save the files
    """
    file = None
    if not os.path.isfile(file_name):
        # If file_name does not exists, create
        file = codecs.open(
            file_name,
            'w+',
            encoding='UTF-8'
        )
        print("Creating {}".format(file_name))
        if initial_template_file_name:
            render_template_with_args_in_file(file, initial_template_file_name, **{})
    else:
        # If file exists, just load the file
        file = codecs.open(
            file_name,
            'a+',
            encoding='UTF-8'
        )

    return file


def generic_insert_module(module_name, args, **kwargs):
    """
    In general we have a initial template and then insert new data, so we dont repeat the schema for each module
    :param module_name: String with module name
    :paran **kwargs: Args to be rendered in template
    """
    file = create_or_open(
        os.path.join(
            args['django_application_folder'],
            '{}.py'.format(module_name),
        ),
        os.path.join(
            BASE_TEMPLATES_DIR,
            '{}_initial.py.tmpl'.format(module_name)
        ),
        args
    )

    render_template_with_args_in_file(
        file,
        os.path.join(
            BASE_TEMPLATES_DIR,
            '{}.py.tmpl'.format(module_name)
        ),
        **kwargs
    )
    file.close()


def check_class_in_file(file_path, class_name):
    try:
        file_to_scan = open(file_path)
        content = file_to_scan.read()
        parsed_tree = ast.parse(content)
        model_exists = False
        for node in ast.walk(parsed_tree):
            if isinstance(node, ast.ClassDef):
                if node.name == class_name:
                    model_exists = True

        return model_exists
    except IOError:
        print("File {} can't be open".format(file_path))
        sys.exit(1)


def sanity_check(args):
    """
    Verify if the work folder is a django app.
    A valid django app always must have a models.py file
    :return: None
    """
    # Validate is an django application folder
    if not os.path.isfile(
            os.path.join(
                args['django_application_folder'],
                'models.py'
            )
    ):
        print("django_application_folder is not a Django application folder")
        sys.exit(1)

    # Validate model Exists
    models_file_path = os.path.join(
        args['django_application_folder'],
        'models.py'
    )

    if not check_class_in_file(models_file_path, args["model_name"]):
        print("Model does not exists")
        sys.exit(1)


def generic_insert_with_folder(folder_name, file_name, template_name, checking_classes, args):
    """
    In general if we need to put a file on a folder, we use this method
    """
    # First we make sure views are a package instead a file
    if not os.path.isdir(
            os.path.join(
                args['django_application_folder'],
                folder_name
            )
    ):
        os.mkdir(os.path.join(args['django_application_folder'], folder_name))
        codecs.open(
            os.path.join(
                args['django_application_folder'],
                folder_name,
                '__init__.py'
            ),
            'w+'
        )
    full_file_name = os.path.join(
        args['django_application_folder'],
        folder_name,
        '{}.py'.format(file_name)
    )
    view_file = create_or_open(
        full_file_name,
        '',
        args
    )

    if functools.reduce(
            operator.and_,
            map(
                check_class_in_file,
                (full_file_name,) * len(VIEW_CLASSES),
                checking_classes
            )
    ):
        print("All classes {} already on file {}".format(", ".join(checking_classes), file_name))
        return 0

    # Load content from template
    render_template_with_args_in_file(
        view_file,
        os.path.join(
            BASE_TEMPLATES_DIR,
            template_name
        ),
        model_name=args['model_name'],
        model_prefix=args['model_prefix'],
        model_name_lower=args['model_name'].lower(),
        application_name=args['django_application_folder'].split("/")[-1]
    )
    view_file.close()
    return 1


def api(args):
    pass


def execute_from_command_line(django_application_folder, type='dashboard', slug=False, create_api=False, mixins=False):
    models = apps.get_models()
    for model in models:
        args = {}
        # If model prefix is not defined, we'll going to define model_prefix as
        # model_name in uppercase
        args['model_name'] = str(model.__name__)
        args['type'] = str(type)
        args['model_prefix'] = str(model.__name__).upper()
        args['django_application_folder'] = django_application_folder
        args['url_pattern'] = str(model.__name__).lower()
        # Views has an specific logic, so we don't touch it
        simplified_file_name = convert(str(model.__name__).strip())
        args["simplified_view_file_name"] = simplified_file_name
        models_file_path = os.path.join(
            args['django_application_folder'],
            'models.py'
        )
        simplified_file_name = convert(args['model_name'].strip())
        args["simplified_view_file_name"] = simplified_file_name

        if check_class_in_file(models_file_path, str(model.__name__)):
            sanity_check(args)
            generic_insert_with_folder(
                "views",
                simplified_file_name,
                "view.py.tmpl",
                VIEW_CLASSES,
                args
            )
            permission_class_name = "{}Permission".format(args["model_name"])
            flag = generic_insert_with_folder(
                "tests",
                "test_{}".format(simplified_file_name),
                "tests.py.tmpl",
                [permission_class_name],
                args
            )
            if flag != 0:
                inject_modules(args, create_api, mixins, simplified_file_name, slug)
                if type == 'dashboard':
                    copy_account(args)
                    copy_templates(args)
                copy_template_tags(args)


def inject_modules(args, create_api, mixins, simplified_file_name, slug):
    modules_to_inject = [
        'conf',
        'forms',
        'admin'
    ]
    if slug:
        modules_to_inject.append('urls_slug')
    else:
        modules_to_inject.append('urls')
    if create_api:
        modules_to_inject += [
            'serializers',
            'viewsets',
            'urls_api'
        ]
    if mixins:
        modules_to_inject.append('mixins')
    for module in modules_to_inject:
        generic_insert_module(
            module,
            args,
            model_name=args['model_name'],
            model_prefix=args['model_prefix'],
            url_pattern=args['url_pattern'],
            view_file=simplified_file_name,
            model_name_lower=args['model_name'].lower()
        )
    # This is just a fix to link api_urls with urls
    if create_api:
        render_template_with_args_in_file(
            create_or_open(
                os.path.join(
                    args['django_application_folder'],
                    BASE_TEMPLATES_DIR,
                    'urls.py'
                ),
                "",
                args
            ),
            os.path.join(
                BASE_TEMPLATES_DIR,
                "urls_api_urls_patch.py.tmpl"
            )
        )


def copy_account(args):
    if not os.path.isdir(
            os.path.join(
                args['django_application_folder'],
                'templates',
                'account')):
        os.mkdir(
            os.path.join(
                args['django_application_folder'],
                'templates',
                'account')
        )
    for basic in [
        'login.html', 'password_change.html', 'password_reset.html', 'signup.html',
    ]:
        original = os.path.join(
            'base_django',
            'templates',
            'dashboard',
            'account',
            basic
        )
        target = os.path.join(
            args['django_application_folder'],
            'templates',
            'account'
        )
        shutil.copy(original, target)


def copy_templates(args):
    for basic in [
        '404.html', '500.html', 'base.html', 'base_error.html', 'loading.html', 'breadcrumb.html', 'menu.html'
    ]:
        original = os.path.join(
            'base_django',
            'templates',
            'dashboard',
            basic
        )
        target = os.path.join(
            args['django_application_folder'],
            'templates',
            basic
        )
        shutil.copy(original, target)

    for item in VIEW_CLASSES:
        if not os.path.isdir(
                os.path.join(
                    args['django_application_folder'],
                    'templates',
                    convert(args['model_name'].strip().lower()))):
            os.mkdir(
                os.path.join(
                    args['django_application_folder'],
                    'templates',
                    convert(args['model_name'].strip().lower()))
            )
        original = os.path.join(
            'base_django',
            'templates',
            'dashboard',
            'model',
            convert(item.strip().lower() + '.html')
        )
        target = os.path.join(
            args['django_application_folder'],
            'templates',
            convert(args['model_name'].strip().lower()),
            convert(item.strip().lower() + '.html')
        )
        shutil.copy(original, target)


def copy_template_tags(args):
    for item in ['form_utils.py', 'input_checker.py', 'math_utils.py', 'type_utils.py']:
        original = os.path.join(
            'base_django',
            'templatetags',
            item
        )
        target = os.path.join(
            args['django_application_folder'],
            'templatetags',
            item
        )
        if not os.path.isdir(
                os.path.join(
                    args['django_application_folder'],
                    'templatetags')):
            os.mkdir(
                os.path.join(
                    args['django_application_folder'],
                    'templatetags'
                )
            )
            init_file = codecs.open(
                os.path.join(
                    args['django_application_folder'],
                    'templatetags',
                    '__init__.py'
                ),
                'w+'
            )
            init_file.close()
        shutil.copy(original, target)
