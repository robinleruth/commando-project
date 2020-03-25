import os


from flask import Flask

from app.infrastructure.config import app_config
from app.infrastructure.log import logger


def create_app(config=app_config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config)

    from app.interface.web.routes import bp as main_bp
    app.register_blueprint(main_bp)
    from app.interface.web.backtester_bp import bp as backtester_bp
    app.register_blueprint(backtester_bp)
    from app.interface.web.stream_logs import bp as log_bp
    app.register_blueprint(log_bp)

    logger.info('start up')

    logger.info('Creating graph folder')
    os.makedirs(app_config.GRAPH_FOLDER, exist_ok=True)

    return app
