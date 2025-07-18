from django.contrib import admin
from .models import Product # CORINNE JUL 10: imported Product model to admin panel
from .models import List, ListItem # LYSS: For my lists


admin.site.register(Product) # CORINNE JUL 10: imported Product model to admin panel

# LYSS: These are also for my lists

admin.site.register(List)
admin.site.register(ListItem)


