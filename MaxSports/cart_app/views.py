from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from product_app.models import product_sizes_variants, product_color_image
from accounts.models import user_address
from .models import Cart, Cart_products, Wishlist, Coupons
from wallet.models import Wallet_User, Wallet_transactions
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from category_app.models import category
from django.http import JsonResponse
import json
import logging
from django.db.models import Count
from django.utils import timezone
from decimal import Decimal
from django.core.exceptions import ObjectDoesNotExist
from order_app.models import Order
from django.db.models import Q, Subquery
from django.views.decorators.cache import never_cache
from datetime import datetime

# Create your views here.
logger = logging.getLogger(__name__)
date_now = (timezone.now()).date()


# ======    SHOW CART     ====== #


@never_cache
@login_required
def cart_show(request):
    storage = messages.get_messages(request)
    storage.used = True

    user = request.user
    try:
        user_cart = Cart.objects.get(user_id=user)
    except Cart.DoesNotExist:
        cart = Cart(user_id=user)
        cart.save()
        user_cart = Cart.objects.get(user_id=user)
    cart_total = user_cart.total_amount
    available_coupons = Coupons.objects.filter(
        min_limit__lte=cart_total,
        max_limit__gte=cart_total,
        expiry__gte=date_now,
        valid_from__lte=date_now,
        is_active=True,
    )

    cart_all = Cart_products.objects.filter(cart=user_cart).order_by("-id")
    for product in cart_all:
        if (
            not product.product_color_variant.product_data_id.status
            or product.product_color_variant.product_data_id.delete_opt
        ):
            product.delete()
            messages.info(
                request,
                "Sorry, "+
                f"{product.product_color_variant.product_data_id}"+
                " is currently unavailable to buy",
            )

        if product.product_color_variant.product_quantity == 0:
            product.delete()
            messages.info(
                request,
                f"Sorry, {product.product_color_variant.product_data_id} is currently unavailable to buy",
            )
    cart_all = Cart_products.objects.filter(cart=user_cart).order_by("-id")
    
    context = {
        "user_cart": user_cart,
        "cart_all": cart_all,
        "category_data": category.objects.filter(is_listed=True),
        "available_coupons": available_coupons
    }
    if user_cart:
        return render(request, "user/cart.html", context)
    else:
        return redirect("home")


# ======  END SHOW CART  ====== #


# ====== ADD PRODUCT CART ====== #


@login_required
def add_product_to_cart(request):
    storage = messages.get_messages(request)
    storage.used = True

    if request.method == "POST":
        user_in_action = User.objects.get(username=request.user)
        product_id_to_add = request.POST.get("product_id")
        product_size = request.POST.get("product_size")
        redirect_wishlist = request.POST.get("redirect_wishlist")

        try:
            user_selected_product = product_sizes_variants.objects.get(
                product_data_id=product_id_to_add, product_size=product_size
            )

        except ObjectDoesNotExist:
            user_selected_product = product_sizes_variants.objects.get(
                id=product_id_to_add
            )
        if not Cart.objects.filter(user_id=request.user).exists():
            new_cart = Cart()
            new_cart.user_id = user_in_action
            new_cart.save()

        user_cart = Cart.objects.get(user_id=user_in_action)
        cart_products_count = Cart_products.objects.filter(cart=user_cart).aggregate(
            num_items=Count("id")
        )["num_items"]

        if Cart_products.objects.filter(
            product_color_variant=user_selected_product, cart=user_cart
        ):
            messages.error(request, "Product already added to the cart")
            if redirect_wishlist is not None:
                return redirect("show_wishlist")
            return redirect("product_details", product_id_to_add)
        elif cart_products_count > 9:
            messages.error(
                request,
                "Cart is overloaded,Finish the purchase" + " or remove few products",
            )
            if redirect_wishlist is not None:
                return redirect("show_wishlist")
            return redirect("product_details", product_id_to_add)
        price = user_selected_product.product_data_id.product_id.product_price_after()
        Cart_products.objects.get_or_create(
            cart=user_cart,
            product_color_variant=user_selected_product,
            sub_total=float(price),
        )
        user_cart.total_amount = user_cart.total_amount + Decimal(price)
        user_cart.total_amount_without_coupon = user_cart.total_amount
        user_cart.save()
        messages.success(request, f"{user_selected_product} added to cart")
        if redirect_wishlist is not None:
            return redirect("show_wishlist")
        return redirect("product_details", product_id_to_add)


# ====== END ADD PRODUCT ====== #


# ======    REMOVE CART     ====== #


@login_required
def remove_from_cart(request):
    delete_id = request.GET.get("delete_id")

    if not delete_id:
        messages.error(request, "Invalid cart item ID.")
        return redirect("cart_show")

    try:
        cart_product = Cart_products.objects.get(id=delete_id)
    except Cart_products.DoesNotExist:
        messages.error(request, "Cart item not found.")
        return redirect("cart_show")

    try:
        users_cart = Cart.objects.get(user_id=request.user)
    except Cart.DoesNotExist:
        messages.error(request, "Your cart does not exist.")
        return redirect("cart_show")

    if cart_product.cart != users_cart:
        messages.error(request, "Unauthorized cart item removal.")
        return redirect("cart_show")

    users_cart.total_amount -= cart_product.sub_total
    users_cart.total_amount_without_coupon = users_cart.total_amount
    users_cart.save()
    cart_product.delete()

    messages.success(request, "Item removed from cart successfully.")
    return redirect("cart_show")


# ======  END REMOVE CART  ====== #


# ====== UPDATE TOTAL PRICE  ====== #

@login_required
def update_total_price(request):
    storage = messages.get_messages(request)
    storage.used = True

    if request.method != "POST":
        return redirect("cart_show")

    try:
        data = json.loads(request.body)
        quantity = int(data.get("quantity"))
        product_id = data.get("productId")
        user = request.user

        cart = Cart.objects.get(user_id=user)
        cart_item = Cart_products.objects.get(id=product_id, cart=cart)
    except (Cart.DoesNotExist, Cart_products.DoesNotExist, ValueError, TypeError):
        return JsonResponse({"stockError": True, "message": "Invalid cart item."})

    product_variant = cart_item.product_color_variant
    available_stock = product_variant.product_quantity
    price = product_variant.product_data_id.product_id.product_price_after()

    if quantity > 10 and available_stock > 10:
        quantity = 10
    elif quantity > available_stock:
        quantity = available_stock

    if not product_variant.product_data_id.status or product_variant.product_data_id.delete_opt:
        cart_item.delete()
        return JsonResponse({
            "stockError": True,
            "message": "Product is no longer available.",
        })

    total_price = quantity * price
    cart_item.quantity = quantity
    cart_item.sub_total = total_price
    cart_item.save()

    all_cart_items = Cart_products.objects.filter(cart=cart)
    total_amount_final = 0.00
    for item in all_cart_items:
        item_price = item.product_color_variant.product_data_id.product_id.product_price_after()
        total_amount_final += item.quantity * item_price

    if total_amount_final < 4999:
        total_amount_final += 150

    cart.total_amount = total_amount_final
    cart.total_amount_without_coupon = total_amount_final
    cart.save()

    available_coupons = Coupons.objects.filter(
        min_limit__lte=total_amount_final,
        max_limit__gte=total_amount_final,
        expiry__gte=date_now,
        valid_from__lte=date_now,
        is_active=True,
    )

    coupons_data = []
    for coupon in available_coupons:
        coupons_data.append({
            "code": coupon.code,
            "title": coupon.title,
            "discount_amount": coupon.discount_amount if coupon.discount_amount else None,
            "discount_percentage": coupon.discount_percentage if coupon.discount_percentage else None,
        })

    if quantity != int(data.get("quantity")):
        return JsonResponse({
            "stockError": True,
            "message": f"Only {quantity} item(s) available.",
            "availableQuantity": quantity,
            "totalPrice": total_price,
            "subTotal": str(total_amount_final),
            "updatedQuantity": quantity,
            "availableCoupons": coupons_data,
        })

    return JsonResponse({
        "success": True,
        "totalPrice": total_price,
        "subTotal": str(total_amount_final),
        "availableCoupons": coupons_data,
    })


# ====== END UPDATE TOTAL PRICE ====== #


# ======  APPLY COUPON  ====== #

@login_required
def apply_coupon(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            coupon_code = data.get("coupon", None)
            user = request.user
            user_cart = Cart.objects.get(user_id=user)

            coupon_obj = Coupons.objects.get(code=coupon_code)

            if Order.objects.filter(user_id=user, coupon_name=coupon_obj).exists():
                return JsonResponse({"error": "You already used this coupon."})

            if not coupon_obj.min_limit <= user_cart.total_amount:
                return JsonResponse({"error": "Minimum amount not satisfied."})

            if not coupon_obj.max_limit > user_cart.total_amount:
                return JsonResponse({"error": "Maximum amount exceeded."})

            if Cart.objects.filter(user_id=request.user, coupon=coupon_obj).exists():
                return JsonResponse({"error": "Coupon already applied."})

            # Reset amount
            user_cart.total_amount = user_cart.total_amount_without_coupon

            if coupon_obj.discount_amount:
                discount = coupon_obj.discount_amount
                user_cart.total_amount -= discount
            else:
                discount = coupon_obj.discount_percentage
                user_cart.total_amount -= (user_cart.total_amount * discount / 100)

            user_cart.coupon = coupon_obj
            user_cart.coupon_active = True
            user_cart.save()

            return JsonResponse({
                "message": f"Coupon {coupon_obj.code} applied!",
                "total": f"₹ {user_cart.total_amount}",
                "coupon": {
                    "coupon_code": coupon_obj.code,
                    "coupon_discount": f"₹{discount}" if coupon_obj.discount_amount else f"{discount}%"
                }
            })

        except Exception as e:
            return JsonResponse({"error": str(e)})

    return JsonResponse({"error": "Invalid request method."})


# ====== END APPLY COUPON ====== #


# ====== DELETE COUPON ====== #

@login_required
def delete_coupon(request):
    if request.method == "POST":
        user_cart = Cart.objects.get(user_id=request.user)
        user_cart.total_amount = user_cart.total_amount_without_coupon
        user_cart.remove_coupon()
        user_cart.save()
        return JsonResponse({"message": "Coupon removed", "total": f"₹ {user_cart.total_amount}"})
    return JsonResponse({"error": "Invalid request method."})

# ====== END COUPON ====== #


#  << ====== CHECKOUT  ====== >>

# ====== ADD CHECKOUT PRODUCT ====== #

# ====== END CHECKOUT PRODUCT ====== #


# ======    CHECKOUT PRODUCT     ====== #
@never_cache
@login_required
def checkout_product(request):
    storage = messages.get_messages(request)
    storage.used = True

    try:
        user = request.user
        user_addresses = user_address.objects.filter(
            user_id=user, delete_address=False
        ).order_by("-id")

        cart = Cart.objects.get(user_id=user)
        users_cart = Cart_products.objects.filter(cart=cart)
        if not users_cart:
            messages.info(request, "Add products in cart first !!")
            return redirect("cart_show")
        final_sum = cart.total_amount
        coupon = cart.coupon
        try:
            if cart.coupon.discount_amount:
                coupon_discount = cart.coupon.discount_amount
            else:
                coupon_discount = cart.coupon.discount_percentage
        except AttributeError:
            coupon_discount = None
        context = {
            "user_addresses": user_addresses,
            "cart_all": users_cart,
            "total_sum": final_sum,
            "final_sum": final_sum,
            "coupon": coupon,
            "coupon_discount": coupon_discount,
            "wallet": Wallet_User.objects.get(user_id=request.user),
        }
    except Cart.DoesNotExist:
        return redirect("cart_show")
    return render(request, "user/checkout.html", context)


# ======    END CHECKOUT     ====== #

#  << ====== Wishlist  ====== >>


# ======    SHOW WISHLIST     ====== #


@login_required
@never_cache
def show_wishlist(request):
    storage = messages.get_messages(request)
    storage.used = True

    users_wishlist = Wishlist.objects.filter(user=request.user)
    size_variants = []
    for wishlist_item in users_wishlist:
        product_color_variant = wishlist_item.product_color_variant
        size = product_sizes_variants.objects.filter(
            product_data_id=product_color_variant
        )
        size_variants.extend(size)
    context = {
        "all_wishlist": users_wishlist,
        "size_variants": size_variants,
    }
    return render(request, "user/wishlist.html", context)


# ====== END SHOW WISHLIST ====== #


# ======     ADD TO WISHLIST    ====== #


@login_required
def add_to_wishlist(request, product_id):
    product = product_color_image.objects.get(id=product_id)
    created = False

    if not Wishlist.objects.filter(user=request.user, product_color_variant=product).exists():
        Wishlist.objects.create(user=request.user, product_color_variant=product)
        created = True

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if created:
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'exists'}, status=400)
    else:
        next_url = request.GET.get("next") or "/"
        if created:
            messages.success(request, "Product added to wishlist successfully")
        else:
            messages.error(request, "Product already exists in your wishlist.")
        return redirect(next_url)



# ====== END ADD TO WISHLIST ====== #


# ====== END ADD TO WISHLIST ====== #


@login_required
def delete_from_wishlist(request):
    storage = messages.get_messages(request)
    storage.used = True

    try:
        delete_id = request.GET.get("delete_id", None)
        cart_product = Wishlist.objects.get(id=delete_id)
        cart_product.delete()
        return redirect("show_wishlist")
    except Wishlist.DoesNotExist:
        messages.error(request, "Couldn't delete cart item")
        return redirect("show_wishlist")


# ====== END ADD TO WISHLIST ====== #
