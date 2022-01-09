from django.conf import settings
import traceback

from django.core.exceptions import PermissionDenied
from django.http import Http404
from rest_framework import exceptions
from rest_framework.views import exception_handler as drf_exception_handler

from sentry_sdk import capture_exception


def exception_handler(exc, context):
    """
    API Exception handling according to RFC 7807:
    https://datatracker.ietf.org/doc/html/rfc7807

    Inspired by drf-problems:
    https://github.com/shivanshs9/drf-problems/

    Adapted here for explicity and customizablity
    Especially error reports to sentry.io
    """
    # Convert Django exceptions (from DRF).
    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()
    elif not isinstance(exc, exceptions.APIException):
        capture_exception(exc)
        exc = exceptions.APIException(exc)

    # Log full exceptions to console
    if settings.DEBUG:
        print(traceback.format_exc())

    request = context['request']
    response = drf_exception_handler(exc, context)
    data = response.data

    problem_title = getattr(exc, 'title', exc.default_detail)
    problem_status = response.status_code
    if isinstance(data, dict):
        data['title'] = problem_title
        data['status'] = problem_status
    else:
        data = {
            "errors": response.data,
            "title": problem_title,
            "status": problem_status,
        }
    try:
        if request.accepted_renderer.format == 'json':
            response.content_type = 'application/problem+json'
    except AttributeError:
        pass
    response.data = data

    return response
