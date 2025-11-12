import re
from collections.abc import Callable, Iterable
from re import Pattern

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect


class LoginRequiredMiddleware:
    """
    Redirect anonymous users to LOGIN_URL unless the request path matches an
    exempt pattern. Paths are matched against request.path_info.lstrip('/').
    Place after AuthenticationMiddleware and before other app middlewares.
    """

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]):
        self.get_response = get_response
        patterns: Iterable[str] = getattr(settings, "LOGIN_REQUIRED_EXEMPT_URLS", [])
        self._exempt: list[Pattern[str]] = [re.compile(p) for p in patterns]

    def __call__(self, request: HttpRequest) -> HttpResponse:
        # If authenticated, allow
        if request.user.is_authenticated:
            return self.get_response(request)

        # Normalize path for matching
        path = request.path_info.lstrip("/")

        # If any pattern matches, allow
        for pattern in self._exempt:
            if pattern.match(path):
                return self.get_response(request)

        # Otherwise, redirect to login with next
        return redirect(f"{settings.LOGIN_URL}?next={request.get_full_path()}")
