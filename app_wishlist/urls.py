from django.urls import path
from .views import (
    wishlist_view,
    wishlist_view_json,
    wishlist_add_view_json,
    wishlist_del_view_json
)

app_name = 'app_wishlist'

urlpatterns = [
    path('', wishlist_view, name='wishlist'),
    path('api/', wishlist_view_json, name='wishlist_api'),
    path('api/add/<int:id_product>/', wishlist_add_view_json, name='wishlist_add'),
    path('api/del/<int:id_product>/', wishlist_del_view_json, name='wishlist_del'),
]
