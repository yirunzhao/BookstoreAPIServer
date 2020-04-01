### This is an experimental assignment of computer network experiment of Wuhan University


### Environment: Python 3.7 / Django 2.2.7


### Contributor: WHU.CS.Ryan 

---


# 网上书店API接口文档

- 基准地址：http://yrzhao.club:8000/api/bookstore/

| *状态码* | *含义* | *说明*                 |
| -------- | ------ | ---------------------- |
| 200      | OK     | 为了简化，代表一切成功 |
| 233      | ERROR  | 为了简化，代表一切失败 |

## 用户管理

### 登陆

- 路径：auth/login/
- 方法：post
- 请求参数

| 参数名    | 参数说明 | 备注     |
| --------- | -------- | -------- |
| telephone | 用户电话 | 不能为空 |
| password  | 密码     | 不能为空 |

请求示例：

```js
data(){
	return{
		userForm:{
			telephone:1888888888,
			password:'123123'
		}
	}
},
methods:{
	async getUserList(){
    // 需要配置axios挂载到Vue对象，并且baseURL=基础URL
    const {data:res} = await this.$http.get('login',{params : userForm})
  }
}
```

- 响应参数

| 参数名    | 说明   | 备注 |
| --------- | ------ | ---- |
| id        | 用户id |      |
| username  | 用户名 |      |
| telephone | 电话   |      |
| email     | 邮箱   |      |

成功返回值示例：

```json
{
  data:{
   	"id":110,
    "username":"aaa",
   	"telephone":"1888888888",
    "email":"123123@qq.com"
  },
  meta:{
  	"status":200,
    "message":"lotegin succeed!"
	}
}
```





### 注册

- 路径：auth/register/
- 方法：post
- 参数

| 参数名    | 参数说明 | 备注     |
| --------- | -------- | -------- |
| username  | 用户名   | 不能为空 |
| password  | 密码     | 不能为空 |
| telephone | 电话     | 不能为空 |
| email     | 邮箱     |          |

请求示例：

```js
data(){
	return{
		userRegForm:{
			username:'aaa',
			password:'123123',
      telephone:'1888888888',
      email:'123123@qq.com'
		}
	}
},
methods:{
	async Register(){
    // 需要配置axios挂载到Vue对象,设置为$http，并且baseURL=基础URL
    const {data:res} = await this.$http.get('login',userRegForm)
  }
}
```

- 响应参数

| 参数名    | 说明   | 备注 |
| --------- | ------ | ---- |
| id        | 用户id |      |
| username  | 用户名 |      |
| telephone | 电话   |      |
| email     | 邮箱   |      |

成功返回示例：

```json
{
  data:{
    "id":110,
    "username":"aaa",
   	"telephone":"1888888888",
    "email":"123123@qq.com"
  },
  meta:{
    status:201,
    message:"register succeed!"
  }
}
```



### 用户编辑个人信息

- 路径：auth/modify/
- 方法：post
- 参数

| 参数名       | 参数说明       | 备注             |
| ------------ | -------------- | ---------------- |
| uid          | 用户 ID        | 不能为空，不能改 |
| username     | 修改后的用户名 |                  |
| password     | 修改后的密码   |                  |
| telephone    | 修改后的电话   |                  |
| 修改后的邮箱 |                |                  |

请求示例

```js
data(){
	return{
		userModifyForm:{
      id:111
			username:'aaa',
			password:'123123',
      telephone:'1888888888',
      email:'123123@qq.com'
		}
	}
},
methods:{
	async modify(){
    // 需要配置axios挂载到Vue对象,设置为$http，并且baseURL=基础URL
    const {data:res} = await this.$http.put(`users/${this.userModifyForm.id}`,{username:this.userModifyForm.username,password:this.userModifyForm.password,telephone:this.userModifyForm.telephone,email:this.userModifyForm.email})
    // 就是把表单数据都这样提交了
    
  }
}
```



- 响应参数

| 参数名    | 说明   | 备注 |
| --------- | ------ | ---- |
| id        | 用户id |      |
| username  | 用户名 |      |
| telephone | 电话   |      |
| email     | 邮箱   |      |



成功返回示例

```json
{
   data:{
      "id":110,
      "username":"aaa",
      "telephone":"1888888888",
      "email":"123123@qq.com"
    },
    meta:{
      status:200,
      message:"modify succeed!"
    } 
}
```

## 书本管理

### 获得全部书本数据

- 路径：books/
- 方法：get
- 参数

| 参数名 | 参数说明 | 备注                                   |
| ------ | -------- | -------------------------------------- |
| query  | 查询参数 | 可以为空，不为空的时候代表根据书名查找 |

- 响应参数

| 参数名      | 说明         | 备注                                             |
| ----------- | ------------ | ------------------------------------------------ |
| id          | 书本id       |                                                  |
| title       | 书籍标题     |                                                  |
| publisher   | 出版社       |                                                  |
| author      | 作者         |                                                  |
| price       | 价格         |                                                  |
| count       | 库存         |                                                  |
| category    | 分类         |                                                  |
| category_id | 分类的id号   |                                                  |
| total       | 返回书本总数 |                                                  |
| comment     | 评论         |                                                  |
| content     | 内容简介     |                                                  |
| author_info | 作者简介     |                                                  |
| catalogue   | 目录         | 为了简化，返回一个列表，每一个元素是一个目录标题 |
| pagenum     | 页数         |                                                  |
| url         | 封面路径     | 在服务器上的路径                                 |

成功返回示例

```json
{
    "data": {
        "total": 3,
        "books": [
            {
                "id": 1,
                "title": "西游记",
                "publisher": "武汉大学出版社",
                "author": "曹雪芹",
                "price": 12.0,
                "category": 12.0,
                "category_id": 1,
                "author_info": "清代文学家，写了红楼梦",
                "comment": [
                    {
                        "customer": "yirunzhao",
                        "content": "收到扶桑岛国搜ID和法国i是否iu感受到佛iu规划史蒂夫关怀送到护肤归属地",
                        "time": "2020-03-21T15:47:05.928Z"
                    },
                    {
                        "customer": "yirunzhao",
                        "content": "第二条评论",
                        "time": "2020-03-21T16:07:32.315Z"
                    }
                ],
                "catalogue": [
                    "第一回:哈哈",
                    "第二回:暗示法",
                    "第三回:sadasd"
                ]
            },
            {
                "id": 2,
                "title": "水浒传",
                "publisher": "北京大学出版社",
                "author": "施耐庵",
                "price": 132.0,
                "category": 132.0,
                "category_id": 1,
                "author_info": "水浒传水浒传",
                "comment": [],
                "catalogue": []
            },
            {
                "id": 3,
                "title": "程序设计艺术",
                "publisher": "武汉大学出版社",
                "author": "Knuth",
                "price": 342.0,
                "category": 342.0,
                "category_id": 2,
                "author_info": "句老俱老俱老big ",
                "comment": [],
                "catalogue": []
            }
        ]
    },
    "meta": {
        "status": 200,
        "message": "获得全部书籍信息成功"
    }
}
```

### 获得一本书的书本数据

- 路径：books/one/:id
- 方法：get
- 参数

| 参数名 | 参数说明 | 备注 |
| ------ | -------- | ---- |
| id     | 书籍id   |      |

- 响应参数

```json
{
    "data": {
        "id": 2,
        "title": "水浒传",
        "publisher": "北京大学出版社",
        "author": "施耐庵",
        "price": 132.0,
        "category": "文学",
        "category_id": 1,
        "author_info": "水浒传水浒传",
        "comment": [],
        "catalogue": []
    },
    "meta": {
        "status": 200,
        "message": "获得单个书籍成功"
    }
}
```

### 获取全部分类

- 路径：books/getcate/
- 方法：get
- 无请求参数
- 响应参数

| 参数名      | 说明   | 备注 |
| ----------- | ------ | ---- |
| category    | 分类名 |      |
| category_id | 分类id |      |
|             |        |      |



### 获得某一分类书本数据

- 路径：books/category/
- 方法：get
- 参数

| 参数名 | 参数说明 | 备注 |
| ------ | -------- | ---- |
| id     | 分类id   |      |

- 响应参数

| 参数名      | 说明         | 备注                                                         |
| ----------- | ------------ | ------------------------------------------------------------ |
| id          | 书本id       |                                                              |
| title       | 书籍标题     |                                                              |
| publisher   | 出版社       |                                                              |
| author      | 作者         |                                                              |
| price       | 价格         |                                                              |
| count       | 库存         |                                                              |
| category    | 分类         |                                                              |
| category_id | 分类id       |                                                              |
| total       | 返回书本总数 |                                                              |
| comment     | 评论         |                                                              |
| content     | 内容简介     |                                                              |
| author_info | 作者简介     |                                                              |
| catalogue   | 目录         | 为了简化，返回一个列表，每一个元素是一个目录标题，存储使用longtext，每一个章节由"\|"分开 |
| pagenum     | 页数         |                                                              |

成功返回示例

```json
{
    "data": {
        "total": 2,
        "books": [
            {
                "id": 1,
                "title": "西游记",
                "publisher": "武汉大学出版社",
                "author": "曹雪芹",
                "price": 12.0,
                "category": 12.0,
                "category_id": 1,
                "author_info": "清代文学家，写了红楼梦",
                "comment": [
                    {
                        "customer": "yirunzhao",
                        "content": "收到扶桑岛国搜ID和法国i是否iu感受到佛iu规划史蒂夫关怀送到护肤归属地",
                        "time": "2020-03-21T15:47:05.928Z"
                    },
                    {
                        "customer": "yirunzhao",
                        "content": "第二条评论",
                        "time": "2020-03-21T16:07:32.315Z"
                    }
                ],
                "catalogue": [
                    "第一回:哈哈",
                    "第二回:暗示法",
                    "第三回:sadasd"
                ]
            },
            {
                "id": 2,
                "title": "水浒传",
                "publisher": "北京大学出版社",
                "author": "施耐庵",
                "price": 132.0,
                "category": 132.0,
                "category_id": 1,
                "author_info": "水浒传水浒传",
                "comment": [],
                "catalogue": []
            }
        ]
    },
    "meta": {
        "status": 200,
        "message": "获取分类书籍成功"
    }
}
```



### 评论

- 路径：books/comment/
- 方法：post
- 请求参数

| 参数名  | 说明         | 备注 |
| ------- | ------------ | ---- |
| user_id | 评论的用户id |      |
| book_id | 评论的书籍id |      |
| content | 评论详情     |      |

返回示例

应该不需要返回数据，检查meta就行了

```json
{
  data:{
    
  },
  meta:{
    status:200,
    message:"comment succeed!"
  }
}
```

## 购物车与购买

### 查看当前用户的购物车信息

- 路径：orders/:id
- 方法：get
- 请求参数

| 参数名 | 参数说明 | 备注                  |
| ------ | -------- | --------------------- |
| id     | 用户 ID  | 不能为空`携带在url中` |

- 响应参数

| 参数名 | 说明     | 备注                                                 |
| ------ | -------- | ---------------------------------------------------- |
| id     | 书籍id   | 先提前获取所有书籍信息，根据id就可以得到单个书籍信息 |
| date   | 下单时间 |                                                      |
| count  | 下单数量 |                                                      |
| total  | 书本种类 |                                                      |

```json
{
    "data": {
        "total": 2,
        "books": [
            {
                "book_id": 1,
                "title": "西游记",
                "url": "http://yrzhao.club/static/images/1.jpg",
                "publisher": "武汉大学出版社",
                "author": "曹雪芹",
                "price": 12.0,
                "category": "文学",
                "category_id": 1,
                "count": 10
            },
            {
                "book_id": 2,
                "title": "水浒传",
                "url": "http://yrzhao.club/static/images/1.jpg",
                "publisher": "北京大学出版社",
                "author": "施耐庵",
                "price": 132.0,
                "category": "文学",
                "category_id": 1,
                "count": 22
            }
        ]
    },
    "meta": {
        "status": 200,
        "message": "ok"
    }
}
```

### 删除商品

- 路径：orders/delete/
- 方法：post
- 请求参数

| 参数名 | 说明   | 备注 |
| ------ | ------ | ---- |
| userid | 用户id |      |
| bookid | 书籍id |      |

### 修改商品个数

- 路径：orders/modify/
- 方法：post
- 请求参数

| 参数名  | 说明         | 备注 |
| ------- | ------------ | ---- |
| user_id | 用户id       |      |
| book_id | 书籍id       |      |
| count   | 修改后的个数 |      |



### 加入购物车

- 路径：orders/add/
- 方法：post
- 请求参数

| 参数名  | 说明                    | 备注 |
| ------- | ----------------------- | ---- |
| user_id | 用户id                  |      |
| book_id | 书籍id                  |      |
| count   | 购买数量                |      |
| books   | 存放bookid和count的数组 |      |

请求数据示例(Json)

```json
{
  user_id: 123,
  books: [
  	{book_id:123,count:10},
    {book_id:233,count:22},
  ]
}
```



返回示例

```json
{
  data:{
    
  },
  meta:{
    status:200,
    message:"add book succeed!"
  }
}
```

### 把购物车中选中物品添加到订单中

- 路径：orders/commit/
- 方法：post
- 请求参数

| 参数名  | 说明       | 备注           |
| ------- | ---------- | -------------- |
| user_id | 用户id     |                |
| books   | 书籍id列表 |                |
| address | 地址       | 直接让用户输入 |

请求json示例

```json
{
	"user_id":gsdsdf,
  "books": [1,2,3,4],
  "address": "wuhan university"
}
```

- 返回参数

| 参数名   | 说明   | 备注 |
| -------- | ------ | ---- |
| order_id | 订单id |      |

返回示例

```json
{
  data:{
    order_id:123
  },
  meta:{
    status:200,
    message:"buy book succeed!"
  }
}
```

### 购买

- 路径：orders/purchase/
- 方法：post
- 请求参数

| 参数名   | 说明   | 备注 |
| -------- | ------ | ---- |
| user_id  | 用户id |      |
| order_id | 订单id |      |

请求示例json

```
{
	"user_id":asfasfas,
	"order_id":1
}
```

### 查看购买历史

- 路径：orders/history/
- 方法：get
- 请求参数

| 参数名  | 说明   | 备注 |
| ------- | ------ | ---- |
| user_id | 用户id |      |

- 响应参数

| 参数名    | 说明     | 备注 |
| --------- | -------- | ---- |
| title     | 书籍名称 |      |
| date      | 购买日期 |      |
| count     | 购买数量 |      |
| author    | 作者     |      |
| publisher | 出版商   |      |
| price     | 价格     |      |
| category  | 分类     |      |

返回示例

```json
{
    "data": {
        "total": 6,
        "books": [
            {
                "title": "西游记",
                "author": "曹雪芹",
                "price": 12.0,
                "publisher": "武汉大学出版社",
                "category": "文学",
                "date": "2020-03-22T08:02:18.067Z"
            },
            {
                "title": "水浒传",
                "author": "施耐庵",
                "price": 132.0,
                "publisher": "北京大学出版社",
                "category": "文学",
                "date": "2020-03-22T08:02:18.071Z"
            },
            {
                "title": "西游记",
                "author": "曹雪芹",
                "price": 12.0,
                "publisher": "武汉大学出版社",
                "category": "文学",
                "date": "2020-03-22T08:31:23.576Z"
            },
            {
                "title": "水浒传",
                "author": "施耐庵",
                "price": 132.0,
                "publisher": "北京大学出版社",
                "category": "文学",
                "date": "2020-03-22T08:31:23.579Z"
            },
            {
                "title": "水浒传",
                "author": "施耐庵",
                "price": 132.0,
                "publisher": "北京大学出版社",
                "category": "文学",
                "date": "2020-03-22T08:41:49.476Z"
            },
            {
                "title": "程序设计艺术",
                "author": "Knuth",
                "price": 342.0,
                "publisher": "武汉大学出版社",
                "category": "计算机科学",
                "date": "2020-03-22T08:41:49.480Z"
            }
        ]
    },
    "meta": {
        "status": 200,
        "message": "获取历史成功！"
    }
}
```

