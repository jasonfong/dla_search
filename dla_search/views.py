from django import http
import django
from django.core.cache import cache
from datetime import datetime
from dla_search.dla_data import DLAData
from dla_search.http_helpers import get_url_text, JsonResponse
from dla_search.models import Restaurant
from datetime import datetime


def home(request):
    cache.set('foo', 'bar')
    return http.HttpResponse('Time now is: {}, got this from memcache: {}'.format(datetime.now(), cache.get('foo')))


def clear_cache(request):
    cache.clear()
    return http.HttpResponse('Cache cleared')


def update_db(request):
    dla = DLAData()
    data = dla.get_summary_list()

    for item in data:
        r = Restaurant.query(Restaurant.name == item.get('name')).get()

        if r is None:
            r = Restaurant()

        r.populate(
            name = item.get('name'),
            lunch_price = item.get('lunch_price'),
            dinner_price = item.get('dinner_price'),
            cuisine = item.get('cuisine'),
            neighborhood = item.get('neighborhood'),
            details_path = item.get('details_path'),
            has_yelp = False,
        )
        r.put()

    return JsonResponse(data)


def update_yelp(request):
    name = request.GET['name']

    r = Restaurant.query(Restaurant.name == name).get()

    dla = DLAData()
    yelp_data = dla.get_yelp_data(r.details_path)

    r.populate(
        has_yelp = True,
        yelp_url = yelp_data['yelp_url'],
        yelp_rating = yelp_data['yelp_rating'],
        addr_street = yelp_data['addr_street'],
        addr_city = yelp_data['addr_city'],
        addr_state = yelp_data['addr_state'],
        addr_postal = yelp_data['addr_postal'],
        yelp_updated = datetime.now(),
    )
    r.put()

    return JsonResponse(yelp_data)





def dinela_home(request):
    text = get_url_text('http://www.discoverlosangeles.com/dinela-los-angeles-restaurant-week')
    return http.HttpResponse(text)
    