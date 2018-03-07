# single

## 环境配置
1.添加配置文件

```
cp config/dev.tpl.py env.py
```
2.如果是本地开发环境，可以将 SQLALCHEMY_DATABASE_URI 设置成 'sqlite:///dog.db'

3.数据库迁移
```
FLASK_APP=dog.py flask upgrade
```
4.启动后端服务器
```
FLASK_APP=dog.py flask run
```

