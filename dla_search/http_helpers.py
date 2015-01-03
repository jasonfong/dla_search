import json
from django.http import HttpResponse
import urllib2
from django.conf import settings


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


def get_url_text(url):
    req = urllib2.Request(url)
    req.add_header('User-agent', settings.USER_AGENT)
    res = urllib2.urlopen(req)
    url_text = res.read()
    return url_text


def get_url_json(url):
    return json.loads(get_url_text(url))
