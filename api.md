# API
```
无特殊说明，请求Content-Type:application/json
```
## 一、app管理
### 1.1 申请app
```
POST /create/app
```
BODY
```
{
  "name":"应用名称",
}
```
RESPONSE
```
{
  "app_id":"fadf12",
  "public_key":"公钥，可提供给前端进行加密重要数据",
  "private_key":"私钥，禁止泄露"
}
```

## 二、用户管理
所有接口中均需在header中添加如下字段：

APPID:app_id
TOKEN:{{token}}

### 2.1 生成token
token有效时间5分钟，超过指定时间的token会返回403错误
```
将当前时间的字符串（精确到秒）使用private_key进行RSA加密。
时间格式如:
  '1575964041'
```
### 2.1 新增用户
```
POST /user
```
BODY
```
{
  "name":"用户名",
  "key":"公钥加密(SHA256(密码)@时间)",
  "email":"邮箱"
}
```
### 2.2 重置用户密码
```
PATCH /user/resetpasswd
```
BODY
```
{
  "user_id":"用户编号",
  "oldkey":"公钥加密(SHA256(旧密码)@时间)",
  "newkey":"公钥加密(SHA256(新密码)@时间)"
}
```
### 2.3 删除用户
```
DELETE /user
```
BODY
{
  "user_id":"用户编号",
}
### 2.4 用户列表
```
GET /user?page=1&size=20
```
RESPONSE
```
{
  "data":[
    {'user_id':'','name':'','email':'','createdAt':'','lastLogin':'','remark':''}
   ],
  "page":"1",
  "pageSize":"20",
  "total":"200",
  "totalPage":"10"
}
```
### 2.5 修改用户
```
PATCH /user
```
BODY
```
{
  "user_id":"用户编号",
  "remark":"",
  "email":"",
  "name":"",
}
```
