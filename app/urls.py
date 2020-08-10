from django.urls import path

from . import conf

urlpatterns = [

]

from .views import category

urlpatterns += [
    # category
    path(
        'category/',
        category.List.as_view(),
        name=conf.CATEGORY_LIST_URL_NAME
    ),
    path(
        'category/create/',
        category.Create.as_view(),
        name=conf.CATEGORY_CREATE_URL_NAME
    ),
    path(
        'category/<int:pk>/',
        category.Detail.as_view(),
        name=conf.CATEGORY_DETAIL_URL_NAME
    ),
    path(
        'category/<int:pk>/update/',
        category.Update.as_view(),
        name=conf.CATEGORY_UPDATE_URL_NAME
    ),
    path(
        'category/<int:pk>/delete/',
        category.Delete.as_view(),
        name=conf.CATEGORY_DELETE_URL_NAME
    ),
]

