#!/usr/bin/env python
# -*- coding: utf-8 -*-
import django_filters
import django_tables2 as tabs
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.utils.html import format_html
from django_filters.views import FilterView
from django_tables2 import tables, LazyPaginator, SingleTableView

from base_django.views import BaseCreateView, BaseDeleteView, BaseDetailView, BaseUpdateView, BaseListView

try:
    from django.core.urlresolvers import reverse_lazy
except ImportError:
    from django.urls import reverse_lazy, reverse

from .. import (models, forms, conf)


class CategoryFilter(django_filters.FilterSet):
    class Meta:
        model = models.Category
        fields = ('id', 'created_at',)


class ActionsColumn(tabs.Column):

    def __init__(self):
        super(ActionsColumn, self).__init__(orderable=False, empty_values=(), verbose_name='Acoes')

    def render(self, record):
        return format_html('<a class="btn btn-info btn-xs" href="{}"><span class="glyphicon glyphicon-edit"></span> Editar</a> <a href="{}" class="btn btn-danger btn-xs"><span class="glyphicon '
                           'glyphicon-remove"></span> Remover</a>', reverse(conf.CATEGORY_DETAIL_URL_NAME, kwargs={'pk': record.pk}),
                           reverse(conf.CATEGORY_DELETE_URL_NAME, kwargs={'pk': record.pk})
                           )


class CategoryTable(tables.Table):
    actions = ActionsColumn()

    class Meta:
        model = models.Category
        template_name = "django_tables2/bootstrap.html"
        fields = ('id', 'created_at', 'published_at',)
        orderable = True
        order_by = '-created_ad'
        row_attrs = {
            "data-id": lambda record: record.pk
        }
        attrs = {
            'id': 'table',
            'class': 'table'
        }


class List(LoginRequiredMixin, FilterView, BaseListView, SingleTableView):
    """
    List all Categorys
    """
    table_class = CategoryTable
    paginator_class = LazyPaginator
    filterset_class = CategoryFilter

    queryset = models.Category.objects.all()
    template_name = 'category/list.html'
    model = models.Category
    context_object_name = 'categorys'
    ordering = '-created_at'

    def get_queryset(self):
        return models.Category.objects.all()

    def get_context_data(self, **kwargs):
        context = super(List, self).get_context_data(**kwargs)

        context['detail_url_name'] = conf.CATEGORY_DETAIL_URL_NAME

        if self.request.user.has_perm("app.add_category"):
            context['create_object_reversed_url'] = reverse_lazy(
                conf.CATEGORY_CREATE_URL_NAME
            )
        
        return context


class Create(LoginRequiredMixin, PermissionRequiredMixin, BaseCreateView):
    """
    Create a Category
    """
    model = models.Category
    permission_required = (
        'app.add_category'
    )
    form_class = forms.CategoryForm
    template_name = 'category/create.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super(Create, self).get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse_lazy(conf.CATEGORY_DETAIL_URL_NAME, kwargs=self.kwargs_for_reverse_url())

    def get_initial(self):
        data = super(Create, self).get_initial()
        return data

    def form_valid(self, form):
        messages.success(self.request, 'Category criado com sucesso')
        return super(Create, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Houve algum erro, tente novamente')
        return super(Create, self).form_invalid(form)


class Detail(LoginRequiredMixin, BaseDetailView):
    """
    Detail of a Category
    """
    model = models.Category
    template_name = 'category/detail.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super(Detail, self).get_context_data(**kwargs)

        if self.request.user.has_perm("app.change_category"):
            context['update_object_reversed_url'] = reverse_lazy(
                conf.CATEGORY_UPDATE_URL_NAME,
                kwargs=self.kwargs_for_reverse_url()
            )

        if self.request.user.has_perm("app.delete_category"):
            context['delete_object_reversed_url'] = reverse_lazy(
                conf.CATEGORY_DELETE_URL_NAME,
                kwargs=self.kwargs_for_reverse_url()
            )
        return context


class Update(LoginRequiredMixin, PermissionRequiredMixin, BaseUpdateView):
    """
    Update a Category
    """
    model = models.Category
    template_name = 'category/update.html'
    context_object_name = 'category'
    form_class = forms.CategoryForm
    permission_required = (
        'app.change_category'
    )

    def get_initial(self):
        data = super(Update, self).get_initial()
        return data

    def get_success_url(self):
        return reverse_lazy(conf.CATEGORY_DETAIL_URL_NAME, kwargs=self.kwargs_for_reverse_url())

    def get_context_data(self, **kwargs):
        data = super(Update, self).get_context_data(**kwargs)
        return data

    def form_valid(self, form):
        messages.success(self.request, 'Category atualizado com sucesso')
        return super(Update, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Houve algum erro, tente novamente')
        return super(Update, self).form_invalid(form)


class Delete(LoginRequiredMixin, PermissionRequiredMixin, BaseDeleteView):
    """
    Delete a Category
    """
    model = models.Category
    permission_required = (
        'app.delete_category'
    )
    template_name = 'category/delete.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super(Delete, self).get_context_data(**kwargs)
        return context

    def __init__(self):
        super(Delete, self).__init__()

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Category removido com sucesso')
        return super(Delete, self).delete(self.request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy(conf.CATEGORY_LIST_URL_NAME)
