from flask import Flask
import website.api_keys


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = api_keys.secret_key

    from .views import views
    
    app.register_blueprint(views, url_prefix='/')
    return app


