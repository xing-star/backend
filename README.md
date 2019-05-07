## 后台服务器

- 安装virtualenv
`pip install virtualenv`

- 创建虚拟环境
`Windows 环境下: virtualenv myvenv` 
`Mac 环境下: python3 -m venv myvenv` 
-(会在当前目录下生成myvenv的文件夹)
************
- 激活虚拟环境(Windows)
  1.`cd myvenv\Scripts`
  2.`activate`
  3. 此时可查看到一个克隆本地电脑的干净Python环境 `pip list` (查看当前虚拟环境安装的Python包)
  4. 退出虚拟环境`deactivate`
- 激活虚拟环境(Mac)
  1.`source myvenv/bin/activate`

- 之后生成新的虚拟环境可通过
`pip install -r requirements.txt`
(即可一键安装所需依赖包)

#### 使用Flask-Migrate实现数据库的迁移，可用于创建以及更新表的操作，之后无需手动创建表结构。

1. 修改Development模式下的数据库配置，进入config.py文件
```
Line 18: mysql+pymysql://<MYSQL_USER>:<MYSQL_PWD>@localhost:3306/inspection 修改为本机的数据库位置用户名密码端口
如果没有inspection 数据库创立，用 create database inspection CHARACTER SET utf8mb4 创建数据库
```

2.`python manage.py db init` (创建迁移仓库, 如果出现 `Error: Directory migrations already exists` 删除文件目录中已经存在的migration文件夹，重新执行命令) 
```
正确输出
\  Creating directory /Users/vzhehao/Developer/Workspace/audio_analysis_server/migrations ... done
  Creating directory /Users/vzhehao/Developer/Workspace/audio_analysis_server/migrations/versions ... done
  Generating /Users/vzhehao/Developer/Workspace/audio_analysis_server/migrations/script.py.mako ... done
  Generating /Users/vzhehao/Developer/Workspace/audio_analysis_server/migrations/env.py ... done
  Generating /Users/vzhehao/Developer/Workspace/audio_analysis_server/migrations/README ... done
  Generating /Users/vzhehao/Developer/Workspace/audio_analysis_server/migrations/alembic.ini ... done
  Please edit configuration/connection/logging settings in
  '/Users/vzhehao/Developer/Workspace/audio_analysis_server/migrations/alembic.ini' before proceeding.
```

3.`python manage.py db migrate -m "initial migration"`(创建迁移脚本，需先创建改数据库不然会报改数据库不存在)
```
正确输出
INFO  [alembic.runtime.migration] Context impl MySQLImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.autogenerate.compare] Detected added table 'permissions'
INFO  [alembic.autogenerate.compare] Detected added table 'roles'
INFO  [alembic.autogenerate.compare] Detected added table 'task'
INFO  [alembic.autogenerate.compare] Detected added table 'text_analyzer'
INFO  [alembic.autogenerate.compare] Detected added table 'users'
  Generating /Users/vzhehao/Developer/Workspace/audio_analysis_server/migrations/versions/daa860541898_initial_migration.py ... done
```

4.`python manage.py db upgrade`(更新数据库)
```
正确输出
INFO  [alembic.runtime.migration] Context impl MySQLImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> daa860541898, initial migration
```

5. 手动查看db 确认表结构已经被注册

- 至此数据库已生成所需表结构

- 如变更表结构需要删除数据表与版本控制表再执行2，3的动作
- 已有迁移脚本只需执行3动作即可生成表结构

6. 将seed数据输入数据库
```
mysql -u<MYSQL_USER> -p<MYSQL_PWD> inspection < seed.sql
```


#### 启动开发环境

- 在虚拟环境下并确认安装好requirements.txt中的所有扩展包后在audio_analysis_server路径下
`python manage.py runserver`即可启动。
