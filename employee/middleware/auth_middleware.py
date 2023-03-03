from django.shortcuts import redirect


class SessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, id=None):
        if not request.session.get("email"):
            return redirect("login")
        response = self.get_response(request, id) if id else self.get_response(request)
        return response
