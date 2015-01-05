from django import http
import django
from django.core.cache import cache
from datetime import datetime
from dla_search.dla_data import DLAData
from dla_search.http_helpers import get_url_text, get_url_json, JsonResponse
from dla_search.models import Restaurant
from datetime import datetime, timedelta
from django.conf import settings


def home(request):
    cache.set('foo', 'bar')
    return http.HttpResponse('Time now is: {}, got this from memcache: {}'.format(datetime.now(), cache.get('foo')))


def clear_cache(request):
    cache.clear()
    return http.HttpResponse('Cache cleared')


def update_summary_list(request):
    dla = DLAData()
    data = dla.get_summary_list()
    names =[]

    for item in data:
        r = Restaurant.query(Restaurant.name == item.get('name')).get()

        if r is None:
            r = Restaurant()
            r.has_yelp = False

        r.populate(
            name = item.get('name'),
            lunch_price = item.get('lunch_price'),
            dinner_price = item.get('dinner_price'),
            cuisine = item.get('cuisine'),
            neighborhood = item.get('neighborhood'),
            details_path = item.get('details_path'),
        )
        r.put()
        names.append(r.name)

    return JsonResponse({
        "status": "ok",
        "updated": names,
    })


def update_yelp(request):
    name = request.GET['name']

    r = Restaurant.query(Restaurant.name == name).get()

    dla = DLAData()
    yelp_data = dla.get_yelp_data(r.details_path)

    r.populate(yelp_updated=datetime.now(), **yelp_data)
    r.put()

    return JsonResponse({
        "status": "ok",
        "yelp_data": yelp_data,
    })


def update_yelp_next_batch(request):
    timenow = datetime.now()
    dla = DLAData()
    updated_count = 0

    names = []
    for r in Restaurant.query().fetch():
        try:
            if r.yelp_updated is None or (timenow - r.yelp_updated > timedelta(seconds=settings.YELP_UPDATE_INTERVAL)):
                yelp_data = dla.get_yelp_data(r.details_path)
                r.populate(yelp_updated=datetime.now(), **yelp_data)
                r.put()

                if (yelp_data['has_yelp']):
                    names.append(r.name)
                    updated_count += 1
                    if updated_count >= settings.YELP_UPDATE_BATCH_SIZE:
                        break

        except:
            pass

    return JsonResponse({
        "status": "ok",
        "updated": names,
    })


def clear_data(request):
    for r in Restaurant.query().fetch():
        r.key.delete()

    return JsonResponse({
        "status": "ok",
    })

