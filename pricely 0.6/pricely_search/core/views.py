from django.shortcuts import render, redirect  # CORINNE JUL 10
from .models import Product, List, ListItem  # CORINNE JUL 10 / LYSS: for list
from django.http import HttpResponse, JsonResponse  # CORINNE JUL 11 / EUL JUL 16
from django.template import loader
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required  # LYSS: store List info per user
from celery.result import AsyncResult
from celery import group, chord
from core.tasks import start_scrape_all
import json
import traceback
import re
from django.views.decorators.http import require_POST

# ========== Utility Function ==========

def process_product(product):
    max_length = 40
    name = product['name']
    truncated_name = name if len(name) <= max_length else name[:max_length - 3] + '...'

    price_str = str(product['price'])
    if "$" in price_str:
        try:
            price_value = float(price_str.replace("$", "").replace(",", "").strip())
            price_in_pesos = int(round(price_value * 57))
            display_price = f"₱{price_in_pesos:,}"
        except ValueError:
            display_price = "N/A"
    elif "₱" in price_str:
        display_price = price_str.strip()
    else:
        display_price = f"₱{price_str}"

    rating = product.get('rating', '')

    return {
        **product,
        "truncated_name": truncated_name,
        "display_price": display_price,
        "rating": rating,
    }

# ========== Authenticated Views ==========

@login_required
def index(request):
    search_history = request.session.get("search_history", [])
    return render(request, "core/index.html", {"search_history": search_history})


@login_required
def search_results(request):
    return render(request, "core/search_results.html")


@login_required
def clear_search_history(request):
    if request.method == "POST":
        request.session["search_history"] = []
    return redirect("index")


@login_required
def logout_view(request):
    logout(request)
    return redirect('login_view')


@login_required
def my_lists(request):
    user_lists = List.objects.filter(user=request.user)
    selected_list = None
    items = []

    list_id = request.GET.get("list")
    if list_id:
        try:
            selected_list = user_lists.get(id=list_id)
            items = selected_list.items.all()      
            for item in items:
                item.display_price = convert_price_to_php(item.price)
        except List.DoesNotExist:
            selected_list = None

    return render(request, "core/my_lists.html", {
        "lists": user_lists,
        "selected_list": selected_list,
        "items": items,
    })


@login_required
def get_user_lists(request):
    user = request.user
    lists = user.lists.all().values('id', 'name')
    return JsonResponse({'lists': list(lists)})


@login_required
def start_search(request):
    query = request.GET.get("query", "")
    category = request.GET.get("category", "all categories").strip().lower()

    print(f"[DEBUG] Received query: '{query}', category: '{category}'")
    task_id = start_scrape_all(query, category)
    return JsonResponse({"task_id": task_id})


@login_required
def check_task_status(request):
    task_id = request.GET.get("task_id")
    result = AsyncResult(task_id)

    if result.status == 'SUCCESS':
        return JsonResponse({
            'status': 'done',
            'result': result.result
        })
    elif result.status == 'FAILURE':
        return JsonResponse({
            'status': 'error',
            'message': str(result.result)
        })
    else:
        return JsonResponse({'status': result.status.lower()})


@login_required
def create_list(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            name = data.get("name", "").strip()

            if not name:
                return JsonResponse({"success": False, "error": "List name is required."})

            if List.objects.filter(user=request.user, name=name).exists():
                return JsonResponse({"success": False, "error": "You already have a list with this name."})

            new_list = List.objects.create(name=name, user=request.user)

            return JsonResponse({
                "success": True,
                "list": {
                    "id": new_list.id,
                    "name": new_list.name
                },
                "lists": list(request.user.lists.all().values("id", "name"))
            })
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Invalid request method."})


@login_required
def add_to_list(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            list_id = data.get("list_id")
            product_title = data.get("product_title")
            price = data.get("price")
            rating = data.get("rating")
            product_url = data.get("product_url")
            image_url = data.get("image_url")
            platform = data.get("platform")
            shop_name = data.get("shop_name")

            list_obj = List.objects.get(id=list_id, user=request.user)

            existing = ListItem.objects.filter(
                list=list_obj,
                product_title=product_title,
                product_url=product_url
            ).first()

            if existing:
                return JsonResponse({"message": "This product is already in the list."})

            ListItem.objects.create(
                list=list_obj,
                product_title=product_title,
                price=price,
                rating=rating,
                product_url=product_url,
                image_url=image_url,
                platform=platform,
                shop_name=shop_name,
            )

            return JsonResponse({"message": "Product added to list!"})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


@login_required
def delete_list(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            list_id = data.get("list_id")
            list_obj = List.objects.get(id=list_id, user=request.user)
            list_obj.delete()
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

# ========== Public Views ==========

def login_view(request):
    if request.method == 'GET':
        template = loader.get_template("core/login_view.html")
        context = {}
        return HttpResponse(template.render(context, request))

    elif request.method == 'POST':
        submitted_username = request.POST['username']
        submitted_password = request.POST['password']
        user_object = authenticate(
            username=submitted_username,
            password=submitted_password
        )

        if user_object is None:
            messages.add_message(request, messages.INFO, 'Invalid login.')
            return redirect(request.path_info)

        login(request, user_object)
        return redirect('index')


def signup_view(request):
    if request.method == 'GET':
        template = loader.get_template("core/signup_view.html")
        context = {}
        return HttpResponse(template.render(context, request))

    elif request.method == 'POST':
        submitted_username = request.POST['username']
        submitted_password = request.POST['password']

        if User.objects.filter(username=submitted_username).exists():
            messages.add_message(request, messages.INFO, 'Username already taken.')
            return redirect(request.path_info)

        new_user = User.objects.create_user(username=submitted_username, password=submitted_password)
        login(request, new_user)
        return redirect('index')

@login_required
@require_POST
def remove_item(request, item_id):
    try:
        item = ListItem.objects.get(id=item_id, list__user=request.user)
        item.delete()
        return JsonResponse({"success": True})
    except ListItem.DoesNotExist:
        return JsonResponse({"success": False, "error": "Item not found."}, status=404)

def convert_price_to_php(price):
    usd_to_php = 57  # Use current rate if needed
    price_str = str(price).strip()

    try:
        if price_str.startswith("$"):
            value = float(price_str[1:].replace(",", ""))
            return f"₱{round(value * usd_to_php):,}"
        elif price_str.lower().startswith("usd"):
            value = float(price_str[3:].strip().replace(",", ""))
            return f"₱{round(value * usd_to_php):,}"
        elif "₱" in price_str:
            return price_str  # already formatted
        else:
            return f"₱{price_str}"
    except:
        return "N/A"