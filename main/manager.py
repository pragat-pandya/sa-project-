from main import app, db
from flask_migrate import Migrate
# from flask_script import Manager

migrate = Migrate(app, db)

# manager = Manager(app)
# manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()