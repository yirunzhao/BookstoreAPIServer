from django.db import models
from shortuuidfield import ShortUUIDField


# 书本表
class Book(models.Model):
    title = models.CharField(max_length=30)
    publisher = models.CharField(max_length=30)
    price = models.FloatField(default=66.66)
    # 库存
    count = models.IntegerField(default=0)
    # 页数
    page_num = models.IntegerField()
    # 简介
    content = models.TextField(default='一本不错的书')
    # 封面url
    url = models.CharField(max_length=100, default='http://yrzhao.club/static/images/default.jpg')
    # 目录
    catalogue = models.TextField(null=True)
    # 以下都是外键,一对多关系
    author = models.ForeignKey("Author", on_delete=models.CASCADE)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)

    def __str__(self):
        return self.title


# 作者表
class Author(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()

    def __str__(self):
        return self.name


# 分类表
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Comment(models.Model):
    # 评论内容
    content = models.TextField()
    # 评论时间
    time = models.DateTimeField(auto_now_add=True)
    # 评论人的id
    customer_id = ShortUUIDField()
    # 评论的书籍
    book = models.ForeignKey("Book", on_delete=models.CASCADE)

    def __str__(self):
        return self.book.title
