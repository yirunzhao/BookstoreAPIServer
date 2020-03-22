from django.http import JsonResponse, HttpResponse
import json
from django.contrib.auth import authenticate


def test(request):
    if request.method == 'GET':
        res = {}
        data = {}
        if request.GET.get('name') == 'zyr':
            data['pros'] = 'messi'
            data['university'] = 'CMU/UCB'
            meta = {
                'status': 200,
                'message': 'success'
            }
        elif request.GET.get('name') == 'djc':
            data['pros'] = 'teacher'
            data['university'] = 'WHU'
            meta = {
                'status': 200,
                'message': 'success'
            }
        else:
            meta = {
                'status': 400,
                'message': '没有这个人'
            }
        res['data'] = data
        res['meta'] = meta
        print(request.GET)
        return JsonResponse(res)
    if request.method == 'POST':
        print('成功')
        print(request.body)
        print(type(request.body))
        print(json.loads(request.body))
        return JsonResponse({"wdnmd": "are you ok?"})

    if request.method == 'PUT':
        print('asdasdasdas')
        print(request.body)
        return HttpResponse('ok')


def gettoken(request):
    return HttpResponse('ok')


def get_image(request):
    urls = []
    urls.append('http://yrzhao.club/image/male.jpg')
    return JsonResponse({'urls': urls})


def authtest(request):
    if request.method == 'POST':
        # data = json.loads(request.body)
        # print(data)
        # username = data.get('username')
        # password = data.get('password')
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username,password)
        if username is not None and password is not None:
            is_login = authenticate(request, username=username, password=password)
            if is_login:
                print('ok')
                return HttpResponse('ok')
            else:
                print('fuck')
                return HttpResponse('jjsjsjsj')
        else:
            print('fuck two')
