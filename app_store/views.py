from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from .models import DATABASE
from logic.services import filtering_category
from logic.control_cart import view_in_cart, add_to_cart, remove_from_cart
from django.shortcuts import redirect
from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required


def product_view_json(request):
    if request.method == "GET":
        id_ = request.GET.get("id")
        if id_:
            if id_ in DATABASE:
                return JsonResponse(DATABASE[id_],
                                    json_dumps_params = {'ensure_ascii': False, 'indent': 4})
            return HttpResponseNotFound("Данного товара нет в базе данных")

        category_key = request.GET.get("category")

        if ordering_key := request.GET.get("ordering"):
            reverse = not request.GET.get("reverse", "").lower() == "true"
            data = filtering_category(DATABASE, category_key = category_key, ordering_key = ordering_key, reverse = reverse)
        else:
            data = filtering_category(DATABASE, category_key = category_key)

        return JsonResponse(data, safe = False, json_dumps_params={'ensure_ascii': False, 'indent': 4})

def shop_view(request):
    if request.method == "GET":
        category_key = request.GET.get("category")

        if ordering_key := request.GET.get("ordering"):
            reverse = request.GET.get("reverse") in ('true', 'True')
            data = filtering_category(
                DATABASE,
                category_key,
                ordering_key,
                reverse
            )
        else:
            data = filtering_category(DATABASE, category_key)

        return render(
            request,
            'app_store/shop.html',
            context={
                "products": data,
                "category": category_key})

@login_required(login_url='app_login:login_view')
def cart_view(request):
    if request.method == "GET":
        username = get_user(request).username
        data = view_in_cart(username)[username]

        products = []
        for product_id, quantity in data['products'].items():
            product = DATABASE[product_id].copy()  # важно: копия словаря

            # количество товара
            product["quantity"] = quantity

            # общая стоимость позиции (цена со скидкой * количество)
            product["price_total"] = round(
                product["price_after"] * quantity, 2)

            # добавляем продукт в список
            products.append(product)

        return render(request, "app_store/cart.html", context={"products": products})

def product_page_view(request, page):
    if request.method == "GET":
        product = None

        # поиск продукта
        if isinstance(page, str):
            for data in DATABASE.values():
                if data['html'] == page:
                    product = data
                    break

        elif isinstance(page, int):
            product = DATABASE.get(str(page))

        if not product:
            return HttpResponse(status=404)

        # товары той же категории, кроме текущего
        data_other_products = [
            p for p in DATABASE.values()
            if p["category"] == product["category"]
            and p != product
        ][:5]

        return render(
            request,
            'app_store/product.html',
            context={
                'product': product,
                'other_products': data_other_products
            }
        )

@login_required(login_url='app_login:login_view')
def cart_view_json(request):
    if request.method == "GET":
        username = get_user(request).username
        data = view_in_cart(username)
        return JsonResponse(data, json_dumps_params={'ensure_ascii': False, 'indent': 4})

@login_required(login_url='app_login:login_view')
def cart_add_view_json(request, id_product):
    if request.method == "GET":
        username = get_user(request).username
        if add_to_cart(id_product, username):
            return JsonResponse({"answer": "Продукт успешно добавлен в корзину"},
                                json_dumps_params={'ensure_ascii': False})
        return JsonResponse({"answer": "Неудачное добавление в корзину"},
                            status=404,
                            json_dumps_params={'ensure_ascii': False})

@login_required(login_url='app_login:login_view')
def cart_del_view_json(request, id_product):
    if request.method == "GET":
        username = get_user(request).username
        if remove_from_cart(id_product, username):
            return JsonResponse({"answer": "Продукт успешно удалён из корзины"},
                                json_dumps_params={'ensure_ascii': False})
        return JsonResponse({"answer": "Неудачное удаление из корзины"},
                            status=404,
                            json_dumps_params={'ensure_ascii': False})

def coupon_check_view(request, name_coupon):
    DATA_COUPON = {
        "coupon": {
            "discount": 10,
            "is_valid": True},
        "coupon_old": {
            "discount": 20,
            "is_valid": False},
    }

    if request.method == "GET":
        if name_coupon in DATA_COUPON:
            coupon = DATA_COUPON[name_coupon]
            return JsonResponse({
                "discount": coupon["discount"],
                "is_valid": coupon["is_valid"]
            })
        return HttpResponseNotFound("Неверный купон")

def delivery_estimate_view(request):
    DATA_PRICE = {
        "Россия": {
            "Москва": {"price": 90},
            "Санкт-Петербург": {"price": 78},
            "fix_price": 100,
        },
    }

    if request.method == "GET":
        country = request.GET.get('country')
        city = request.GET.get('city')

        if country not in DATA_PRICE:
            return HttpResponseNotFound("Неверные данные")

        country_data = DATA_PRICE[country]

        if city and city in country_data:
            return JsonResponse({"price": country_data[city]["price"]})

        return JsonResponse({"price": country_data["fix_price"]})

@login_required(login_url='app_login:login_view')
def cart_buy_now_view(request, id_product):
    if request.method == "GET":
        username = get_user(request).username
        result = add_to_cart(id_product, username)
        if result:
            return redirect("app_store:cart_view")

        return HttpResponseNotFound("Неудачное добавление в корзину")

@login_required(login_url='app_login:login_view')
def cart_remove_view(request, id_product):
    if request.method == "GET":
        username = get_user(request).username
        result = remove_from_cart(id_product, username)
        if result:
            return redirect("app_store:cart_view")
        return HttpResponseNotFound("Неудачное удаление из корзины")
# Create your views here.
