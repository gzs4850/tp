import os
from flask_cors import CORS
from app import create_app, db
from app.models import Project,System,Interface,Testcase,Testresult
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
app.debug=True
app.config['JSON_AS_ASCII'] = False
CORS(app)
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db, Project=Project, System=System, Interface=Interface, Testcase=Testcase, Testresult=Testresult)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()