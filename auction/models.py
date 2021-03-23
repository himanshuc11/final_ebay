from django.db import models


# Importing user model from ebay_user
from ebay_user.models import User

# Create your models here.
# Table holding all the categories
class categories(models.Model):
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.category


# Table holding all the listed items
class item(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    minimum_bid = models.IntegerField()
    image_url = models.URLField(max_length=200)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    item_categories = models.ManyToManyField(categories)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.title)


# Table holding all the comments
class comment(models.Model):
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.CharField(max_length=200)
    comment_item = models.ForeignKey(item, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.writer.username)

# Table holding all the bids
class bid(models.Model):
    bid_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    bid_price = models.IntegerField()
    bid_item = models.ForeignKey(item, on_delete=models.CASCADE) 

    def __str__(self):
        return str(self.bid_price)

# Watchlist
class watchlist(models.Model):
    watchlist_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    watclist_items = models.ManyToManyField(item)
