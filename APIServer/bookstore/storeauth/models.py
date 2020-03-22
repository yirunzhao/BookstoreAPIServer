from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from shortuuidfield import ShortUUIDField


class UserManager(BaseUserManager):
    def _create_user(self, telephone, username, password, **kwargs):
        if not telephone:
            raise ValueError('Please input telephone')
        if not username:
            raise ValueError('Please input username')
        if not password:
            raise ValueError('Please input password')
        # 定义user
        user = self.model(telephone=telephone, username=username, **kwargs)
        # 设置密码
        user.set_password(password)
        # 存储到数据库
        user.save()

        return user

    def create_user(self, telephone, username, password, **kwargs):
        kwargs['is_superuser'] = False
        kwargs['is_staff'] = False
        return self._create_user(telephone, username, password, **kwargs)

    def create_superuser(self, telephone, username, password, **kwargs):
        kwargs['is_superuser'] = True
        kwargs['is_staff'] = True
        return self._create_user(telephone, username, password, **kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    # 用户编号
    uid = ShortUUIDField(primary_key=True)
    password = models.CharField(max_length=200)
    telephone = models.CharField(max_length=11, unique=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100)
    # 是否可用
    is_active = models.BooleanField(default=True)
    # 是否是员工
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True)

    # 把内置的username设置为电话号码
    USERNAME_FIELD = 'telephone'
    # 需要输入telephone, username, password
    REQUIRED_FIELDS = ['username']

    EMAIL_FIELD = 'email'

    objects = UserManager()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username



