from google.appengine.ext import ndb


class Restaurant(ndb.Model):
    name = ndb.StringProperty(required=True)
    lunch_price = ndb.FloatProperty()
    dinner_price = ndb.FloatProperty()
    cuisine = ndb.StringProperty(required=True)
    neighborhood = ndb.StringProperty(required=True)
    details_path = ndb.StringProperty(required=True)

    has_yelp = ndb.BooleanProperty(required=True)
    yelp_url = ndb.StringProperty()
    yelp_rating = ndb.FloatProperty()
    addr_street = ndb.StringProperty()
    addr_city = ndb.StringProperty()
    addr_state = ndb.StringProperty()
    addr_postal = ndb.StringProperty()
    yelp_updated = ndb.DateTimeProperty()

    updated = ndb.DateTimeProperty(auto_now=True)
