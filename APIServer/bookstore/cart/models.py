from django.db import models
from APIServer.bookstore.book.models import *
from APIServer.bookstore.storeauth.models import *


# 购物车表和订单表采取简单的设计，里面存储的每一个条目都是一条信息，是多个用户公用的，而不是每个用户持有一个表
# 购物车表
class Cart(models.Model):
    # 书籍，一个订单
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    # 用户
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # 购买数量
    count = models.IntegerField(default=0)
    # 是否加入了订单，默认没有
    # 之后处理提交购物车信息的时候根据这个筛选
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.book.title + '-' + self.user.get_full_name()


# 订单表
class Order(models.Model):
    # 订单生成日期
    time = models.DateTimeField(auto_now_add=True)
    # 是否支付，默认没有
    status = models.BooleanField(default=False)
    # 用户
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # 书籍
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    # 购买的书籍数量
    count = models.IntegerField(default=0)
    # 地址
    address = models.CharField(max_length=150, default='武汉大学计算机学院')
    # 为了代表一次订单的所有条目
    group = models.IntegerField(null=True)

    def __str__(self):
        return self.book.title + '-' + self.user.get_full_name()


# 购买历史表
# 和用户是一对一的
class History(models.Model):
    # 哪个用户
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # 书籍
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    # 购买时间
    time = models.DateTimeField()
    # 数量
    count = models.IntegerField(default=0)
    # 地址
    address = models.CharField(max_length=150, default='武汉大学计算机学院')

    def __str__(self):
        return self.book.title + '-' + self.user.get_full_name()
