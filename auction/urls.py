from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('create/', views.create, name="create"),
    path('description/<str:item_name>', views.item_description, name="item_description"),
    path('bid/<str:item_name>', views.user_bid, name="user_bid"),
    path('close/<str:item_name>', views.close, name="close"),
    path('comment/<str:item_name>', views.item_comment, name="comment"),
    path('add/<str:item_name>', views.add, name="add"),
    path('show_watchlist', views.show_watchlist, name="show_watchlist"),
    path('demo', views.demo, name="demo")
]
