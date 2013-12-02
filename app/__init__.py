#! ../env/bin/python
from flask import Flask, render_template, redirect, url_for

def create_app(object_name, env):
    """
    An flask application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/

    Arguments:
        object_name: the python path of the config object,
                     e.g. appname.settings.ProdConfig

        env: The name of the current environment, e.g. prod or dev
    """

    app = Flask(__name__)

    app.config.from_object(object_name)
    app.config['ENV'] = env

    # Initialize Jinja custom filters
    import filters
    filters.init_app(app)

    # register our blueprints
    from app.blueprints import main
    app.register_blueprint(main)
    
    @app.errorhandler(500)
    def error_handler_500(e):
        return render_template('500.html'), 500

    @app.errorhandler(404)
    def error_handler_404(e):
        return render_template('404.html'), 404

    return app
