from flask import Flask, Blueprint
from flask_restful import Api
from flask_uploads import patch_request_class, configure_uploads


from upload.views import bp,photos


from config import config

def create_app(env):
    app = Flask(__name__)
    app.config.from_object(config[env])

    api_bp = Blueprint('api', __name__)
    api = Api(api_bp)

    # Code for adding Flask RESTful resources goes here

    app.register_blueprint(api_bp, url_prefix="/api/v1")
    app.register_blueprint(bp , url_prefix="/upload2")
    configure_uploads(app, photos)
    patch_request_class(app)
    return app

if __name__ == '__main__':
    app = create_app('development')
    app.run()