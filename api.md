# API
## 一、app管理
### POST 申请app
```
/create/app
```
HEADERS
Content-Type   application/json
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
