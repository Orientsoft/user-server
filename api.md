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
  "id":"fadf12",
  "secert":"密钥，请牢记，后续无接口提供次参数值"
}
```

## 二、用户管理
### 2.1 获取token
token有效时间30分钟
```
GET /token?id={{id}}&secert={{encodeURI(secert)}}
{
  "token":"fadfadfadfadf"
}
```
### 2.1 新增用户
```
POST /user
```
HEADERS

token:{{token}}

BODY
```
{
  "name":"用户名",
  "key":"SHA256(密码)",
  "email":"邮箱"
}
```
