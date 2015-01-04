from dla_search.http_helpers import get_url_text, get_url_json
from bs4 import BeautifulSoup
from django.conf import settings
from datetime import datetime

class DLAData(object):

    def get_summary_list(self):
        index_url = '{}/dinela-los-angeles-restaurant-week?items_per_page={}'.format(settings.DLA_BASEURL, settings.DLA_INDEX_LIMIT)
        index_text = get_url_text(index_url)
        soup = BeautifulSoup(index_text)

        results = []

        for item in soup.select('form.search-form table tbody tr'):
            data = {}

            if 'odd' in item.attrs['class'] or 'even' in item.attrs['class']:

                lunch_price = item.select('td.views-field-field-poi-rw-lunch-price')[0].text.strip()
                if lunch_price:
                    lunch_price = float(lunch_price[1:])
                else:
                    lunch_price = None

                dinner_price = item.select('td.views-field-field-poi-rw-dinner-price')[0].text.strip()
                if dinner_price:
                    dinner_price = float(dinner_price[1:])
                else:
                    dinner_price = None
                
                data['name'] = item.select('td.views-field-title-1 div.title a')[0].text.strip()
                data['lunch_price'] = lunch_price
                data['dinner_price'] = dinner_price
                data['cuisine'] = item.select('td.views-field-field-cuisine')[0].text.strip()
                data['neighborhood'] = item.select('td.views-field-field-neighborhood')[0].text.strip()
                data['details_path'] = item.select('td.views-field-title-1 div.title a')[0].attrs['href']

                results.append(data)

        return results

    def get_yelp_data(self, details_path):
        details_data = { 'has_yelp': False }

        print "getting details"
        details_text = get_url_text('{}/{}'.format(settings.DLA_BASEURL, details_path))
        details_soup = BeautifulSoup(details_text)

        yelp_links = details_soup.select('div.detail-page-yelp a')
        if not yelp_links or len(yelp_links) < 2:
            return details_data

        yelp_url = yelp_links[1].attrs['href']

        if yelp_url == 'http://www.yelp.com/biz/':
            return details_data
 
        print "getting yelp data"
        yelp_data = get_url_json(
            url = 'http://api.yelp.com/v2/business/{}'.format(yelp_url[24:]),
            oauth1 = settings.YELP,
        )

        details_data['has_yelp'] = True
        details_data['yelp_url'] = yelp_url
        details_data['yelp_rating'] = yelp_data['rating']
        details_data['addr_street'] = yelp_data['location']['address'][0]
        details_data['addr_city'] = yelp_data['location']['city']
        details_data['addr_state'] = yelp_data['location']['state_code']
        details_data['addr_postal'] = yelp_data['location']['postal_code']
        details_data['latitude'] = yelp_data['location']['coordinate']['latitude']
        details_data['longitude'] = yelp_data['location']['coordinate']['longitude']
        # details_data['yelp_updated'] = datetime.now()
        
        return details_data


