import json
import os

PATH_WISHLIST = 'wishlist.json'


def view_in_wishlist(username: str = '') -> dict:
    empty_user_wishlist = {'products': []}

    if os.path.exists(PATH_WISHLIST):
        with open(PATH_WISHLIST, encoding='utf-8') as f:
            wishlist = json.load(f)
            if username not in wishlist:
                wishlist[username] = empty_user_wishlist
    else:
        wishlist = {username: empty_user_wishlist}

    with open(PATH_WISHLIST, 'w', encoding='utf-8') as f:
        json.dump(wishlist, f, ensure_ascii=False, indent=4)

    return wishlist


def add_to_wishlist(id_product: str, username: str) -> bool:
    wishlist = view_in_wishlist(username)

    products = wishlist[username]['products']

    id_product = str(id_product)  # 👈 ОБЯЗАТЕЛЬНО

    if id_product not in products:
        products.append(id_product)
        with open(PATH_WISHLIST, 'w', encoding='utf-8') as f:
            json.dump(wishlist, f, ensure_ascii=False, indent=4)
        return True

    return False


def remove_from_wishlist(id_product: str, username: str) -> bool:
    wishlist = view_in_wishlist(username)

    products = wishlist[username]['products']

    id_product = str(id_product)

    if id_product in products:
        products.remove(id_product)
        with open(PATH_WISHLIST, 'w', encoding='utf-8') as f:
            json.dump(wishlist, f, ensure_ascii=False, indent=4)
        return True

    return False