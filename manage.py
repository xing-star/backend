# -*- coding: utf-8 -*-

from api import app, db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

manager = Manager(app)
migrate = Migrate(app, db)


manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    # 使用flask-migrate db迁移工具
    manager.run()
    # 开放内网ip给测试使用
    # app.run(host='0.0.0.0', port=5000, debug='True')
