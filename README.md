# single

## 环境配置
1.添加配置文件

```
cp config/dev.tpl.py env.py 

更改env.py中的配置
```

2.数据库迁移
```
FLASK_APP=dog.py flask upgrade
```
3.启动后端服务器
```
FLASK_APP=dog.py flask run
```

