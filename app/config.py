import os

class BaseConfig:
    ENV_NAME = "base"
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")# 开发可有默认，生产必须用 env 覆盖

class DevelopmentConfig(BaseConfig):
    ENV_NAME = "development"
    DEBUG = True

class ProductionConfig(BaseConfig):
    ENV_NAME = "production"
    DEBUG = False