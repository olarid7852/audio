
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app.app import create_app, register_extensions
from app.config.config import DevelopmentConfig



# def init_db():
#     db.create_all()

if __name__ == '__main__':
    app = create_app(DevelopmentConfig)
    register_extensions(app)
    # PORT = int(app.config['PORT'])
    # app.run(port=PORT)
    manager = Manager(app)
    manager.add_command('db', MigrateCommand)
    manager.run()
    # from src.test import test_update_aud io, client
    # test_update_audio(app.test_client())