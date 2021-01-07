import argparse

from django.core.management.base import BaseCommand, CommandError
from django_crud_generator import execute_from_command_line


class Command(BaseCommand):
    help = 'Script para gerar arquivos'

    def add_arguments(self, parser):
        parser.add_argument(
            '--django_application_folder',
            default="app",
            required=False
        )

        parser.add_argument(
            '--type_template',
            default="dashboard",
            help="Specifies default templates base",
            required=True
        )

        parser.add_argument(
            '--gen_template_default',
            action='store_true',
            help="Create a template default base",
            required=False
        )

        parser.add_argument(
            '--gen_template_model',
            action='store_true',
            help="Create a templates for model",
            required=False
        )

        parser.add_argument(
            '--model_name',
            type=str,
            help="Name of model for make the crud",
            required=True
        )

        parser.add_argument(
            '--model_prefix',
            type=str,
            help="Prefix name for conf variable",
            required=False
        )

        parser.add_argument('--url_pattern', type=str, help="Pattern for url")

        parser.add_argument('--create_api', action='store_true', help="Create a api using Django Rest Framework")

        parser.add_argument('--add_mixins', action='store_true', help="Add mixins to manage nested urls")

        parser.add_argument('--slug', action='store_true', help="Use slug instad pk on urls")

    def handle(self, *args, **options):
        args = dict(options)
        execute_from_command_line(**args)
