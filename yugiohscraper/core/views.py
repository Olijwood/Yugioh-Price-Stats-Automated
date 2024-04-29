from django.shortcuts import render
from django.views import generic

from sets.models import Set
from cards.models import Card, CardImage
# Create your views here.

def set_list_view(request):
    booster_qs = Set.objects.filter(type='Booster')
    premium_qs = Set.objects.filter(type='Premium Pack')
    champion_qs = Set.objects.filter(type='Champion Pack')
    tournament_qs = Set.objects.filter(type='Tournament Pack')
    context = {
        'booster_list': booster_qs,
        'premium_list': premium_qs,
        'champion_list': champion_qs,
        'tournament_list': tournament_qs,
    }
    return render(request, 'index.html', context)

def old_set_detail_view(request, id):
    set = Set.objects.get(id=id)
    card_qs = Card.objects.filter(set=set)
    cards_count = card_qs.count()
    context = {
        'set': set,
        'card_list': card_qs,
        'card_count': cards_count
    }
    return render(request, 'set-detail.html', context)

def older_set_detail_view(request, id):
    set = Set.objects.get(id=id)
    card_qs = Card.objects.filter(set=set)

    # Get the sorting option from the request
    sort_by = request.GET.get('sort_by')
    
    # Apply sorting based on the selected option
    if sort_by == 'name':
        card_qs = card_qs.order_by('card_name')
    elif sort_by == 'code':
        card_qs = card_qs.order_by('card_code')
    elif sort_by == 'price_low':
        card_qs = card_qs.order_by('tcg_market_price')
    elif sort_by == 'price_high':
        card_qs = card_qs.order_by('-tcg_market_price')

    cards_count = card_qs.count()
    context = {
        'set': set,
        'card_list': card_qs,
        'card_count': cards_count
    }
    return render(request, 'set-detail.html', context)

from django.db.models import Count

from django.http import HttpResponseRedirect

def set_detail_view(request, id):
    set_instance = Set.objects.get(id=id)
    card_qs = Card.objects.filter(set=set_instance)

    # Get the sorting option from the request
    sort_by = request.GET.get('sort_by')
    
    # Apply sorting based on the selected option
    if sort_by == 'name':
        card_qs = card_qs.order_by('card_name')
    elif sort_by == 'code':
        card_qs = card_qs.order_by('card_code')
    elif sort_by == 'price_low':
        card_qs = card_qs.order_by('tcg_market_price')
    elif sort_by == 'price_high':
        card_qs = card_qs.order_by('-tcg_market_price')

    # Fetch rarity options and counts for the set
    rarity_options = card_qs.values('card_rarity').annotate(count=Count('card_rarity'))

    # Check if any rarity filter is applied
    selected_rarities = request.POST.getlist('rarity')

    # If rarity filters are selected, filter cards accordingly
    if selected_rarities:
        card_qs = card_qs.filter(card_rarity__in=selected_rarities)

    cards_count = card_qs.count()
    context = {
        'set': set_instance,
        'card_list': card_qs,
        'card_count': cards_count,
        'rarity_options': rarity_options,
        'selected_rarities': selected_rarities
    }
    return render(request, 'set-detail.html', context)