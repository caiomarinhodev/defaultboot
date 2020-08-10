#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.apps import apps
from django.contrib import admin

# Register your models here.
from default.settings import BASE_DIR
from django_crud_generator import execute_from_command_line


def approve_selected(modeladmin, request, queryset):
    queryset.update(is_approved=True)


def desapprove_selected(modeladmin, request, queryset):
    queryset.update(is_approved=False)


approve_selected.short_description = "Aprovar itens selecionados"
desapprove_selected.short_description = "Desaprovar itens selecionados"


class ListAdminMixin(object):
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields]
        self.list_filter = [field.name for field in model._meta.fields if field.name in ['estado', 'cidade', 'status',
                                                                                         'tipo_pagamento',
                                                                                         'forma_pagamento',
                                                                                         'active',
                                                                                         'cupom',
                                                                                         'enviado', 'is_online',
                                                                                         'valor_a_combinar'
                                                                                         'is_approved', 'categoria', 'disponivel', ]]
        self.search_fields = [field.name for field in model._meta.fields if field.name in ['cpf', 'cnpj', 'nome', 'username', 'email',
                                                                                           'name', 'phone', 'titulo', 'descricao', 'telefone', 'telefone_1', ]]
        if len([field.name for field in model._meta.fields if field.name in ['is_approved', ]]) > 0:
            self.actions = [approve_selected, desapprove_selected]
        super(ListAdminMixin, self).__init__(model, admin_site)


models = apps.get_models()
for model in models:
    admin_class = type('AdminClass', (ListAdminMixin, admin.ModelAdmin), {})
    try:
        admin.site.register(model, admin_class)
    except admin.sites.AlreadyRegistered:
        pass

# execute_from_command_line('app', slug=False, create_api=False, mixins=False)
