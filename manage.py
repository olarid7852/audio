
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app.app import create_app, register_extensions
from app.config.config import DevelopmentConfig


if __name__ == '__main__':
    app = create_app(DevelopmentConfig)
    register_extensions(app)
    manager = Manager(app)
    manager.add_command('db', MigrateCommand)
    manager.run()