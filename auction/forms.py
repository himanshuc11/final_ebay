from django.forms import ModelForm
from .models import item

class item_creation_form(ModelForm):
    class Meta:
        model = item
        fields = ['minimum_bid', 'image_url', 'title', 'description', 'item_categories']