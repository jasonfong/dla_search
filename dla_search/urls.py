from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'dla_search.views.home', name='home'),
    url(r'^clear_cache$', 'dla_search.views.clear_cache', name='clear_cache'),
    url(r'^update_db$', 'dla_search.views.update_db', name='update_db'),
    url(r'^update_yelp$', 'dla_search.views.update_yelp', name='update_yelp'),
    url(r'^dinela_home$', 'dla_search.views.dinela_home', name='dinela_home'),
)
