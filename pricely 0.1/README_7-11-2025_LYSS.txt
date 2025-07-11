(models.py)
NOTE: I added these to admin.py; that's also all i did for admin.py

-> LIST: Represents the lists in the list feature we were talking about 
	user = links each list to a logged in user.
		on_delete = if the user is deleted, their lists are deleted too.
		related_name = retrieves all lists created by a user.
	name = the name of the list (LIST 1, LIST 2, LIST 3 in peg).
	created_at = records when the list is created.

-> LISTITEM: Represents a single item (product) in a specific list.
	list = Connects the item to its parent list.
		on_delete = deleting a list deletes its items too.
		related_name = access items in a list like
	product = refers to the actual product being added to the list; this should be another model with the actual product info


(admin.py)
I added these things so the admin can see all of the lists and their list items:
admin.site.register(List)
admin.site.register(ListItem)


(views.py)
my_list = a FUNCTION that focuses on list item retrieval and displaying
	lists = List.objects.filter(user = request.user)
		-> This is my filter; it ensures users only see their own lists
	selected_list_id = request.GET.get("list")
		-> This determines which list among the user's lists IS selected
	selected_list = lists.filter(id=selected_list_id).first()
		-> Basically each list has an ID, so the result for this part depends on selected_list_id
	items = selected_list.items.select_related("product") if selected_list else []
		-> this gets the list of items to display for the next part

return render(request, "core/my_lists.html", ...
	-> this works with items (from above) and the html + CSS to display the list


(urls.py)
path("my-lists/", my_lists, name="my_lists")
	-> I added this for referencing across different files