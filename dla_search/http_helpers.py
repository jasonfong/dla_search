import json
from django.http import HttpResponse
import urllib2
from django.conf import settings
import oauth2


class JsonResponse(HttpResponse):
    def __init__(self, content, status=None, content_type='application/json'):
        super(JsonResponse, self).__init__(
            content=json.dumps(content),
            status=status,
            content_type=content_type,
        )


class JsonErrorResponse(HttpResponse):
    def __init__(self, message, status=500, code=999, name='SYSTEM.INTERNAL_ERROR', content_type='application/json'):

        content = {
            'code': code,
            'name': name,
            'message': message,
        }

        super(JsonErrorResponse, self).__init__(
            content=json.dumps(content),
            status=status,
            content_type=content_type,
        )


def get_url_text(url, oauth1=None):
    if oauth1:
        consumer = oauth2.Consumer(oauth1['CONSUMER_KEY'], oauth1['CONSUMER_SECRET'])
        oauth_request = oauth2.Request(method="GET", url=url)
        oauth_request.update(
            {
                'oauth_nonce': oauth2.generate_nonce(),
                'oauth_timestamp': oauth2.generate_timestamp(),
                'oauth_token': oauth1['TOKEN'],
                'oauth_consumer_key': oauth1['CONSUMER_KEY']
            }
        )
        token = oauth2.Token(oauth1['TOKEN'], oauth1['TOKEN_SECRET'])
        oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
        url = oauth_request.to_url()

    req = urllib2.Request(url)
    req.add_header('User-agent', settings.USER_AGENT)
    res = urllib2.urlopen(req)
    url_text = res.read()
    return url_text


def get_url_json(url, oauth1=None):
    return json.loads(get_url_text(url, oauth1))
