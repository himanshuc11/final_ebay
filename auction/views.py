from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db.models import Max
from django.contrib.auth.decorators import login_required

from .models import comment, item, categories, bid, watchlist
from .forms import item_creation_form

# Create your views here.
def index(request):
    auction_items = item.objects.all()
    return render(request, 'auction/index.html', {'items': auction_items})

def create(request):
    if request.method == "GET":
        form = item_creation_form()
        return render(request, 'auction/create.html', {'form': form})
    if request.method == "POST":
        submitted_form = item_creation_form(request.POST)
        if submitted_form.is_valid():
            user = request.user
            minimum_bid = submitted_form.cleaned_data['minimum_bid']
            image_url = submitted_form.cleaned_data['image_url']
            title = submitted_form.cleaned_data['title']
            description = submitted_form.cleaned_data['description']
            item_categories = submitted_form.cleaned_data['item_categories']

            auction_item = item(owner=user, minimum_bid=minimum_bid, image_url=image_url, title=title, description=description)
            auction_item.save()

            for given_item in item_categories:
                auction_item.item_categories.add(given_item)

            return HttpResponseRedirect(reverse('index'))
        else:
            print(submitted_form.errors)
        return HttpResponse('Response was received')

def item_description(request, item_name):
    required_item = item.objects.get(title=item_name)
    categories = required_item.item_categories.all()

    # Check who is the logged in user
    current_user = request.user
    # Check who is the owner of this particular item
    owner = required_item.owner

    btn = False
    if current_user == owner:
        btn = True

    all_comments = comment.objects.filter(comment_item__title=item_name)
    return render(request, 'auction/item.html', {'item': required_item, 'categories': categories, 'btn': btn, 'comments': all_comments})

@login_required
def user_bid(request, item_name):
    required_bids = bid.objects.filter(bid_item__title=item_name)
    if len(required_bids) > 0:
        # Find bid with maximum value
        current_value = required_bids.aggregate(Max('bid_price'))['bid_price__max']
    else:
        # Return the minimum_bid value attribute
        current_value = item.objects.get(title=item_name).minimum_bid

    if request.method == "GET":
        return render(request, 'auction/user_bid.html', {'current_bid': current_value, 'item_name': item_name})
    else:
        given_value = request.POST['bid']
        if int(given_value) <= current_value:
            return HttpResponse('Your bid is rejected')
        else:
            new_bid = bid(bid_owner=request.user,bid_price=given_value, bid_item=item.objects.get(title=item_name))
            new_bid.save()
            return HttpResponse('Your bid is accepted')

@login_required
def close(request, item_name):
    if request.user != item.objects.get(title=item_name).owner:
        return HttpResponse('You are not authorized to close this auction')

    # All bid on given item
    required_bids = bid.objects.filter(bid_item__title=item_name)
    # What price has the item been sold
    win_value = required_bids.aggregate(Max('bid_price'))['bid_price__max']
    # Which user has won the auction
    winner_name = required_bids.filter(bid_price=win_value)[0].bid_owner

    return HttpResponse(str(winner_name) + " Has won the auction at " + str(win_value))

@login_required
def item_comment(request, item_name):
    if request.method == "GET":
        return render(request, 'auction/comment.html', {'item': item.objects.get(title=item_name)})
    else:
        data = request.POST['comment'] # What exactly did the user comment
        new_comment = comment(writer=request.user, data=data, comment_item=item.objects.get(title=item_name))
        new_comment.save()
        return HttpResponse('Your comment was recorded')
        