from django.shortcuts import render # CORINNE JUL 10
from .models import Product # CORINNE JUL 10: import Product model
from django.shortcuts import redirect # CORINNE JUL 10: for redirecting back to a page

# CORINNE JUL 11: for the login, signup, logout, authenticate features
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required # LYSS: Added this so we can store List info per user! 
from .models import List # LYSS: This one for list

from .utils import scrape_and_rank  # EUL JUL 13: import your unified scraper



# Views that are only visible to authenticated users:

# CORINNE JUL 10
# 1. View for the homepage 
@login_required
def index(request):
    search_history = request.session.get("search_history", [])
    # Render the homepage (index.html) and display search_history (since search_history is a template variable)
    return render(request, "core/index.html", {"search_history": search_history})


# CORINNE JUL 10
# 2. View to handle search and filter products
@login_required
def search_results(request):
    query = request.GET.get("query", "")
    max_price = request.GET.get("max_price")
    min_price = request.GET.get("min_price")
    min_rating = request.GET.get("min_rating")

    products = scrape_and_rank(query) if query else []

    # Apply filters manually since it's no longer a QuerySet
    def filter_product(product):
        try:
            price = float(product["price"].replace("₱", "").replace("$", "").replace(",", "").strip())
        except:
            price = None

        try:
            rating = float(product["rating"].split()[0])  # e.g. "4.5 out of 5 stars"
        except:
            rating = None

        if max_price and price is not None and price > float(max_price):
            return False
        if min_price and price is not None and price < float(min_price):
            return False
        if min_rating and rating is not None and rating < float(min_rating):
            return False

        return True

    filtered_products = [p for p in products if filter_product(p)]

    # Save full search data to session
    if query:
        new_search = {
            "query": query,
            "min_price": min_price,
            "max_price": max_price,
            "min_rating": min_rating,
        }
        history = request.session.get("search_history", [])
        history.insert(0, new_search)
        seen = set()
        unique_history = []
        for item in history:
            key = tuple(item.items())
            if key not in seen:
                seen.add(key)
                unique_history.append(item)
        request.session["search_history"] = unique_history[:10]

    context = {
        "products": filtered_products,
        "query": query,
        "max_price": max_price,
        "min_price": min_price,
        "min_rating": min_rating,
        "rating_options": [5, 4.5, 4, 3.5, 3, 2.5, 2, 1.5, 1], 
    }

    return render(request, "core/search_results.html", context)



# CORINNE JUL 10
# 3. View to clear search history
@login_required
def clear_search_history(request):
    # Checks if a POST request was made (if "Clear Search History" button was clicked)
    if request.method == "POST":
        request.session["search_history"] = [] # Empty the list
    return redirect("index")


# CORINNE JUL 11 
# 4. View to log a user out
@login_required
def logout_view(request):
    logout(request)
    return redirect('login_view')



# Views that are visible to all users:

# CORINNE JUL 11 
# 1. View to log in
def login_view(request):

    # Render login_view.html
    if request.method == 'GET':
        template = loader.get_template("core/login_view.html")
        context = {}
        return HttpResponse(template.render(context, request))
    
    # Checks if a POST request was made (if "Login" button was clicked)
    elif request.method == 'POST':
        # Grab the data
        submitted_username = request.POST['username'] 
        submitted_password = request.POST['password']
        # Authenticate the user
        user_object = authenticate(
            username=submitted_username,
            password=submitted_password
        )

        # If login failed, display the message 'Invalid login'
        if user_object is None: 
            messages.add_message(request, messages.INFO, 'Invalid login.')
            return redirect(request.path_info)
        # If login didn't fail, redirect them to the homepage
        login(request, user_object)
        return redirect('index')
    
# CORINNE JUL 11 
# 2. View to sign up
def signup_view(request):
    
    # Render signup_view.html
    if request.method == 'GET':
        template = loader.get_template("core/signup_view.html")
        context = {}
        return HttpResponse(template.render(context, request))
    
    # Checks if a POST request was made (if "Sign Up" button was clicked)
    elif request.method == 'POST':
        submitted_username = request.POST['username']
        submitted_password = request.POST['password']

        # Checks if username is already taken
        if User.objects.filter(username=submitted_username).exists():
            messages.add_message(request, messages.INFO, 'Username already taken.')
            return redirect(request.path_info)

        # Creates a new user with the submitted data
        new_user = User.objects.create_user(username=submitted_username, password=submitted_password)
        login(request, new_user)
        return redirect('index')




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





