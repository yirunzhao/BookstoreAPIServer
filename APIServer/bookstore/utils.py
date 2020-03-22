from django.http import JsonResponse


def error_return(msg):
    return JsonResponse({"meta": {"status": 233, "message": msg}})


def succeed_return(data, msg):
    return JsonResponse({"data": data, "meta": {"status": 200, "message": msg}})
