from __future__ import annotations

import logging
import os


class Config:
    DEBUG = False
    TESTING = False
    LOGS_LEVEL = logging.INFO

    REDIS_HOST = os.getenv("REDIS_HOST", default="0.0.0.0")  # noqa: S104
    REDIS_PORT = os.getenv("REDIS_PORT", default=59120)

    @staticmethod
    def factory(environment=os.getenv("ENVIRONMENT", "Development")) -> Config:
        match environment:
            case "Development":
                return Development()
            case "Testing":
                return Testing()
            case "Production":
                return Production()
            case _:
                return Config()


class Testing(Config):
    TESTING = True


class Development(Config):
    DEBUG = True
    LOGS_LEVEL = logging.DEBUG


class Production(Config):
    pass
