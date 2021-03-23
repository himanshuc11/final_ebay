from django.contrib import admin
from .models import comment, categories, bid, item, watchlist

# Register your models here.
admin.site.register(comment)
admin.site.register(categories)
admin.site.register(bid)
admin.site.register(item)
admin.site.register(watchlist)