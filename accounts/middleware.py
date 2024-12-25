from rest_framework.response import Response
from django.http import JsonResponse


class ResponseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return self.process_response(request, response)

    def process_response(self, request, response):

        if isinstance(response, Response):
            # Render the response content if it's not rendered
            if not response.is_rendered:
                response.render()

            if 200 <= response.status_code < 300:
                # Success response
                modified_data = {
                    "success": True,
                    "status": response.status_code,
                    "data": response.data
                }
                modified_response = JsonResponse(modified_data, status=response.status_code)
                return modified_response
            else:
                # Error response
                modified_data = {
                    "success": False,
                    "status": response.status_code,
                    "error_data": response.data
                }
                modified_response = JsonResponse(modified_data, status=response.status_code)
                return modified_response

        return response
