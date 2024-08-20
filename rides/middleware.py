# your_app_name/middleware.py

from django.http import HttpResponseNotFound
from django.utils.deprecation import MiddlewareMixin

class AppendSlashMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if response.status_code == 404:
            return HttpResponseNotFound(
                '{"code": 404, "message": "The resource you are looking for was not found."}',
                content_type='application/json'
            )
        return response
