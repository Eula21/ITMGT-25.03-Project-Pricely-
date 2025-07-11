from django.contrib import admin
from .models import Product
from .models import List, ListItem # LYSS: For my lists

admin.site.register(Product)

# LYSS: These are also for my lists

admin.site.register(List)
admin.site.register(ListItem)



