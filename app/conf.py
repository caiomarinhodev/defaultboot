#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

from base_django import conf

CATEGORY_PREFIX = "CATEGORY"

CATEGORY_VERBOSE_NAME = _("Category")
CATEGORY_VERBOSE_NAME_PLURAL = _("Category")

CATEGORY_LIST_URL_NAME = CATEGORY_PREFIX + conf.LIST_SUFFIX
CATEGORY_CREATE_URL_NAME = CATEGORY_PREFIX + conf.CREATE_SUFFIX
CATEGORY_DETAIL_URL_NAME = CATEGORY_PREFIX + conf.DETAIL_SUFFIX
CATEGORY_UPDATE_URL_NAME = CATEGORY_PREFIX + conf.UPDATE_SUFFIX
CATEGORY_DELETE_URL_NAME = CATEGORY_PREFIX + conf.DELETE_SUFFIX
