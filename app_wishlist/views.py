from django.shortcuts import render, redirect
from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from app_store.models import DATABASE
from logic.control_wishlist import view_in_wishlist
from django.http import JsonResponse
from logic.control_wishlist import add_to_wishlist, remove_from_wishlist

@login_required(login_url='app_login:login_view')
def wishlist_view(request):
    if request.method == "GET":
        username = get_user(request).username
        data = view_in_wishlist(username)[username]['products']

        products = []
        for product_id in data:
            product = DATABASE.get(product_id)
            if product:
                products.append(product)

        return render(request, 'app_wishlist/wishlist.html', context={"products": products})

@login_required(login_url='app_login:login_view')
def wishlist_view_json(request):
    username = get_user(request).username
    data = view_in_wishlist(username)[username]
    return JsonResponse(data, json_dumps_params={'ensure_ascii': False, 'indent': 4})

@login_required(login_url='app_login:login_view')
def wishlist_add_view_json(request, id_product):
    username = get_user(request).username
    if add_to_wishlist(id_product, username):
        return JsonResponse({"answer": "Продукт успешно добавлен в избранное"})
    return JsonResponse({"answer": "Неудачное добавление"}, status=404)

@login_required(login_url='app_login:login_view')
def wishlist_del_view_json(request, id_product):
    username = get_user(request).username
    if remove_from_wishlist(id_product, username):
        return JsonResponse({"answer": "Продукт успешно удалён из избранного"})
    return JsonResponse({"answer": "Неудачное удаление"}, status=404)
# Create your views here.
