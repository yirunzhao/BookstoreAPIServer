from django.contrib.auth import authenticate, login
from django.views.decorators.http import require_POST
import json
from .models import User
from APIServer.bookstore.utils import error_return, succeed_return


@require_POST
def login_view(request):
    data = json.loads(request.body)
    try:
        telephone = data['telephone']
        password = data['password']

        user = authenticate(request, username=telephone, password=password)
        if user:
            if user.is_active:
                login(request, user)
                ret = {'id': user.uid, 'username': user.username, 'telephone': user.telephone, 'email': user.email}

                return succeed_return(ret, "登陆成功")
            else:
                return error_return("用户冻结")
        else:
            return error_return("用户不存在")
    except:
        return error_return("有些地方出错了，请联系管理员")


@require_POST
def register_view(request):
    # 获取data
    data = json.loads(request.body)
    # 捕捉异常
    try:
        username = data['username']
        telephone = data['telephone']
        email = data['email']
        password = data['password']
        # 创建用户
        user = User.objects.create_user(telephone, username, password, email=email)
        ret = {'id': user.uid, 'username': user.username, 'telephone': user.telephone, 'email': user.email}

        return succeed_return(ret, "注册成功")
    except KeyError:
        return error_return("创建失败，确保用户名，密码和电话都填写")


@require_POST
def modify_user(request):
    data = json.loads(request.body)

    try:
        uid = data['uid']
        username = data['username']
        telephone = data['telephone']
        email = data['email']
        password = data['password']

        # 获取用户
        user = User.objects.filter(uid=uid, password=password).first()
        # 判断是否存在
        if user is not None:
            exists = User.objects.filter(telephone=telephone).exists()
            if not exists:
                User.objects.filter(uid=uid).update(username=username, telephone=telephone, password=password,
                                                    email=email)
                user = User.objects.filter(uid=uid).first()
                ret = {'id': user.uid, 'username': user.username, 'telephone': user.telephone, 'email': user.email}
                return succeed_return(ret, "修改成功")
            else:
                return error_return("电话号码重复")
        else:
            return error_return("用户名或密码错误")
    except KeyError:
        return error_return("修改失败")
