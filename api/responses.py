from rest_framework import status
from rest_framework.response import Response
from django.http import JsonResponse


def error(msg, status_code=status.HTTP_404_NOT_FOUND):
    return Response({'error': msg}, status=status_code)


def success(msg, status_code=status.HTTP_200_OK):
    return Response(msg, status=status_code)


def json_success(data, status_code=status.HTTP_200_OK, safe=False):
    return JsonResponse(data, safe=False)


def json_error(data, status_code=status.HTTP_404_NOT_FOUND, safe=False):
    return JsonResponse(data, safe=False, status=status_code)
