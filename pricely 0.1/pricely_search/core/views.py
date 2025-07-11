from django.shortcuts import render
from .models import Product
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required # LYSS: Added this so we can store List info per user! 
from .models import List # LYSS: This one for list


def index(request):
    search_history = request.session.get("search_history", [])
    return render(request, "core/index.html", {"search_history": search_history})


def search_results(request):
    query = request.GET.get("query", "")
    max_price = request.GET.get("max_price")
    min_price = request.GET.get("min_price")
    min_rating = request.GET.get("min_rating")

    products = Product.objects.all()
    
    # filter based on query
    if query:
        products = products.filter(product_title__icontains=query)

    # filter based on max price
    if max_price:
        try:
            products = products.filter(price__lte=float(max_price))
        except ValueError:
            pass

    # filter based on min price        
    if min_price:
        try:
            products = products.filter(price__gte=float(min_price))
        except ValueError:
            pass

    # filter based on min rating
    if min_rating:
        try:
            products = products.filter(rating__gte=float(min_rating))
        except ValueError:
            pass

    # Save full search data to session
    if query:
        new_search = {
            "query": query,
            "min_price": min_price,
            "max_price": max_price,
            "min_rating": min_rating,
        }
        history = request.session.get("search_history", [])
        history.insert(0, new_search)  # newest first
        # Remove duplicates while preserving order
        seen = set()
        unique_history = []
        for item in history:
            key = tuple(item.items())
            if key not in seen:
                seen.add(key)
                unique_history.append(item)
        request.session["search_history"] = unique_history[:10]  # limit to last 10

    context = {
        "products": products,
        "query": query,
        "max_price": max_price,
        "min_price": min_price,
        "min_rating": min_rating,
        "rating_options": [5, 4.5, 4, 3.5, 3, 2.5, 2, 1.5, 1], 
    }
    return render(request, "core/search_results.html", context)


def search_history(request):
    history = request.session.get("search_history", [])
    return render(request, "core/search_history.html", {"history": history})


def clear_search_history(request):
    if request.method == "POST":
        request.session["search_history"] = []
    return redirect("index")

# LYSS: Added this function for my list feature as well
# It's the main thing that lets you view different lists from the My Lists page peg I sent

def my_lists(request):
    lists = List.objects.filter(user = request.user)
    selected_list_id = request.GET.get("list")
    selected_list = lists.filter( id= selected_list_id).first()
    items = selected_list.items.select_related("product") if selected_list else []

    return render(request, "core/my_lists.html", {
        "lists": lists,
        "selected_list": selected_list,
        "items": items,
    })
