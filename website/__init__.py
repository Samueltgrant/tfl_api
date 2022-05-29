from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import website.api_keys


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "FSDAJKLJKSFJADK"
    app.config["SQLALCHEMY_DATABASE_URI"] = 'postgres: // byhxcaqmpaygky: 965f695180e2ef9bc0661fca243c36006c6de90b2390c7a5cccdddeaf9a505e8@ec2-34-230-153-41.compute-1.amazonaws.com:5432/d4quaupiqp3lpf'
    db = SQLAlchemy(app)
    migrate = Migrate(app, db)
    from .views import views
    
    app.register_blueprint(views, url_prefix='/')
    return app


