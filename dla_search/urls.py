from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'dla_search.views.home', name='home'),
    url(r'^clear_cache$', 'dla_search.views.clear_cache', name='clear_cache'),
    url(r'^update_summary_list$', 'dla_search.views.update_summary_list', name='update_summary_list'),
    url(r'^update_yelp$', 'dla_search.views.update_yelp', name='update_yelp'),
    url(r'^update_yelp_next_batch$', 'dla_search.views.update_yelp_next_batch', name='update_yelp_next_batch'),
    url(r'^clear_data$', 'dla_search.views.clear_data', name='clear_data'),
)
