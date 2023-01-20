import logging
import os

from flask import Flask

logger = logging.getLogger(__name__)


def create_app(environment: str = os.getenv("ENVIRONMENT", "Development")) -> Flask:
    app = Flask(__name__)
    app.config.from_object(f"url_counter.config.{environment}")
    logger.setLevel(app.config["LOGS_LEVEL"])

    from url_counter.views.api_v1 import api_v1

    app.register_blueprint(api_v1)

    from url_counter.views.reports import reports

    app.register_blueprint(reports)

    from url_counter.views.tests import tests

    app.register_blueprint(tests)

    return app
