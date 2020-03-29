from .models import Author, Category, Book, Comment
from ..storeauth.models import User
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_GET, require_POST
import json
from ..utils import error_return, succeed_return


@require_GET
def get_book(request):
    # 获取查询的书籍名称
    query = request.GET.get('query')
    # 如果有的话,过滤获取信息
    if query:
        books = Book.objects.filter(title__contains=query)
    else:
        # 否则获取全部书籍信息
        books = Book.objects.all()

    data = get_return_data(books)

    return succeed_return(data, "获得全部书籍信息成功")


@require_GET
def select_category(request):
    # 获取分类id
    cate_id = request.GET.get('id')
    exists = Category.objects.filter(id=cate_id).exists()
    if exists:
        category = Category.objects.get(id=cate_id)
        total = category.book_set.count()
        if total == 0:
            return error_return("分类下没有书籍")

        data = get_return_data(books=category.book_set.all())
        return succeed_return(data, "获取分类书籍成功")
    else:
        return error_return("没有这个分类")


# 进行代码复用
# 生成返回数据
def get_return_data(books):
    # 书籍数量
    total = books.count()
    # 返回的书本列表
    ret_books = []
    # 遍历对象获取信息
    for book in books:
        cmt_list = []
        if book.catalogue:
            catalogue_list = book.catalogue.split('|')
        else:
            catalogue_list = []

        for cmt in book.comment_set.all():
            # 没想到怎么优化这个地方，除非改变表
            # 但是我懒得改了
            customer = User.objects.filter(uid=cmt.customer_id).first()
            cmt_list.append({"customer": customer.username, "content": cmt.content, "time": cmt.time})

        ret_books.append({"id": book.id, "title": book.title, "publisher": book.publisher, "author": book.author.name,
                          "price": book.price, "category": book.category.name, "category_id": book.category_id,
                          "author_info": book.author.description, "comment": cmt_list, "catalogue": catalogue_list,
                          "url": book.url})
    data = {
        "total": total,
        "books": ret_books
    }
    return data


@require_GET
def get_one_book(request):
    book_id = request.GET.get('id')
    if book_id is not None:
        book = Book.objects.get(id=book_id)
        if book is not None:
            cmts = []
            for cmt in book.comment_set.all():
                customer = User.objects.get(uid=cmt.customer_id)
                cmts.append({"customer": customer.username, "content": cmt.content, "time": cmt.time})
            if book.catalogue:
                catalogue_list = book.catalogue.split('|')
            else:
                catalogue_list = []
            return JsonResponse({
                "data": {
                    "id": book.id,
                    "title": book.title,
                    "publisher": book.publisher,
                    "author": book.author.name,
                    "price": book.price,
                    "category": book.category.name,
                    "category_id": book.category_id,
                    "author_info": book.author.description,
                    "comment": cmts,
                    "catalogue": catalogue_list,
                    "url": book.url
                },
                "meta": {
                    "status": 200,
                    "message": "获得单个书籍成功"
                }
            })
    else:
        return error_return("book_id没有输入")


@require_POST
def comment(request):
    data = json.loads(request.body)
    if data is not None:
        uid = data.get('user_id')
        book_id = data.get('book_id')
        content = data.get('content')

        book = Book.objects.filter(id=book_id).first()
        if book is not None:
            cmt = Comment(content=content, customer_id=uid, book_id=book_id)
            cmt.book = book
            cmt.save()
            return succeed_return({}, "评论成功")
        else:
            return error_return("没有这本书")
    else:
        return error_return("参数不对")


@require_GET
def get_categories(request):
    categories = []
    for category in Category.objects.all():
        categories.append({'category': category.name, 'category_id': category.id})

    return succeed_return(categories, '获取全部分类成功')
