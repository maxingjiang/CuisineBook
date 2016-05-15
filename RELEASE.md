## VERSION 0.0.1

>接口列表

接口地址 | 参数 | Method | 接口描述
-------- | ---- | ------ | --------
/api/user/authkey | tel | POST | 请求发送验证码
/api/user/register | tel,password,deviceid,code and name,email | POST | 注册账户(tel,password,deviceid,code必填)
/api/user/login | tel,password,deviceid | POST | 登录账户
/api/user/logout | None | POST | 登出账户
/api/user/reset | password | POST | 修改密码，修改成功后会清除Cookies
/api/user/forget | tel,password,code | POST | 忘记密码
/api/user/profile | id | GET | 获取账户信息，忽略id为获取本人信息，非本人操作只能拿到基础信息(id,name,avatar,email)
/api/user/profile | id,name,tel,email,deviceid | POST | 更新账户信息，id必填，其它的有就填没有就不填
/api/user/avatar | id | GET | 获取头像，Content-Type为image/*
/api/user/avatar | avatar | POST | 更新头像，avatar字段内容为Base64编码字符串

1. 使用Cookies作为登录验证，替换原来的TOKEN
2. 添加/log日志访问
3. 验证码过期时间和Cookie过期时间在config.py中配置
4. 去掉了checkkey接口
5. 合并原来的update接口和getuser接口为profile接口
6. getall接口未实现
7. 位置服务和群组服务未实现
8. 除avatar的GET外，返回值格式统一为json格式，包含code,message,result字段，成功的code为0，失败的code暂时为-1

    { "code": 0, "message": "Successfully sent", "result": ok }  
