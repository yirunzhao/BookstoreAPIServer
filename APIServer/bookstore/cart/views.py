from django.views.decorators.http import require_GET, require_POST
import json
from django.db.models import F
from ..utils import *
from .models import *


# 获取用户的购物车信息
@require_GET
def get_carts(request):
    uid = request.GET.get('id')
    user = User.objects.filter(pk=uid).first()
    if user is None:
        return error_return("用户不存在")
    book_list = []
    # 挑出没有提交到订单的书本
    for cart_item in user.cart_set.filter(status=False):
        book_list.append({'book_id': cart_item.book.id, 'title': cart_item.book.title, 'url': cart_item.book.url,
                          'publisher': cart_item.book.publisher, 'author': cart_item.book.author.name,
                          'price': cart_item.book.price, 'category': cart_item.book.category.name,
                          'category_id': cart_item.book.category_id, 'count': cart_item.count})
    data = {
        'total': len(book_list),
        'books': book_list
    }
    return succeed_return(data, "ok")


# 删除购物车中的某一件商品
@require_POST
def delete_book(request):
    data = get_data_from_post(request)
    if data == {}:
        return error_return('参数错误')
    uid = data['user_id']
    book_id = data['book_id']

    return operates('delete', uid, book_id)


# 修改购物车书本个数
@require_POST
def modify_book_count(request):
    data = get_data_from_post(request)
    if data == {}:
        return error_return('参数错误')
    uid = data['user_id']
    book_id = data['book_id']
    count = data['count']

    return operates('update', uid, book_id, count=count)


# 代码复用
def get_data_from_post(request):
    data = json.loads(request.body)
    if data is None:
        return {}
    return data


# 代码复用
def operates(type, uid, book_id, count=0):
    user = User.objects.get(pk=uid)
    book = Book.objects.get(pk=book_id)
    if user is None or book is None:
        return error_return('用户或者书籍不存在购物车中')

    exists = Cart.objects.filter(user=user, book=book).exists()
    if exists:
        if type == 'delete':
            cart_item = Cart.objects.get(user=user, book=book)
            cart_item.delete()
            return succeed_return({}, '删除成功')
        elif type == 'update':
            Cart.objects.filter(user=user, book=book).update(count=count)
            return succeed_return({}, '修改成功')
    else:
        return error_return('购物车信息有误，条目不存在')


# 把书本加入购物车
@require_POST
def add_book(request):
    data = json.loads(request.body)
    if data is not None:
        uid = data['user_id']
        books = data['books']

        user = User.objects.filter(pk=uid).first()
        if user is None:
            return error_return("用户不存在")

        # 遍历每一本书
        for book_item in books:
            book = Book.objects.filter(pk=book_item['book_id']).first()
            # 如果有不存在的，直接报错
            if book is None:
                return error_return("书籍不存在")

            exists = Cart.objects.filter(book=book, user=user).exists()
            # 如果本来就存在，需要相加
            if exists:
                Cart.objects.filter(book=book, user=user).update(count=F("count") + book_item['count'])
            # 不存在，创建新的item
            else:
                cart = Cart(book=book, user=user, count=book_item['count'])
                cart.save()

        return succeed_return({}, "添加成功")
    else:
        return error_return("没有传递参数")


# 提交购物车为订单信息，删除购物车的信息，增加到订单表,包含快递地址
@require_POST
def generate_orders(request):
    data = get_data_from_post(request)
    if data == {}:
        return error_return('参数未传递')
    uid = data['user_id']
    books = data['books']
    address = data['address']

    user = User.objects.filter(pk=uid).first()
    if user is None:
        return error_return('用户不存在')

    if Order.objects.last():
        group = Order.objects.last().group + 1
    else:
        group = 1

    for book_id in books:
        book = Book.objects.filter(pk=book_id).first()
        if book is None:
            return error_return('书籍不存在')

        # 找到购物车条目没有买的书，同一本书只有一条item
        cart = Cart.objects.filter(user=user, book=book, status=False).first()
        if cart is None:
            return error_return('购物车条目不存在')
        # 添加购物车所有书籍到订单表，作为一个item
        # group每次取最后一个+1
        order = Order(book=book, user=user, address=address, count=cart.count, group=group)
        order.save()
        # 更新购物车的status
        Cart.objects.filter(user=user, book=book).update(status=True)

    # 删除所有加入订单的状态
    for added_item in Cart.objects.filter(user=user, status=True):
        added_item.delete()

    return succeed_return({'order_id': group}, '成功')


# 购买，把订单表清除，加入到购买历史表
@require_POST
def purchase(request):
    data = get_data_from_post(request)
    if data == {}:
        return error_return('参数未传递')

    uid = data['user_id']
    order_id = data['order_id']

    user = User.objects.filter(pk=uid).first()
    if user is None:
        return error_return('用户不存在')

    orders = Order.objects.filter(group=order_id)
    if order_id is None:
        return error_return('订单不存在')
    if user.uid != orders.first().user.uid:
        return error_return('用户没有这个订单！')
    # 加入到历史信息表，并删除order信息
    for order in orders:
        # 加入
        history_item = History(time=order.time, book=order.book, count=order.count, user=order.user,
                               address=order.address)
        history_item.save()

        # 删除order
        order.delete()

    return succeed_return({}, '购买成功！')


@require_GET
def get_history(request):
    uid = request.GET.get('user_id')

    user = User.objects.filter(pk=uid).first()
    if user is None:
        return error_return('用户不存在')

    histories = []
    for history_item in user.history_set.all():
        histories.append({'title': history_item.book.title, 'author': history_item.book.author.name,
                          'price': history_item.book.price, 'publisher': history_item.book.publisher,
                          'category': history_item.book.category.name, 'date': history_item.time, 'count': history_item.count})
    data = {
        'total': len(histories),
        'books': histories
    }
    return succeed_return(data, '获取历史成功！')
