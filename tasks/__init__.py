from celery import Celery
import os
from tasks import config

os.environ.setdefault("DJANGO_SETTINGS_MODULE","swiper.settings")

celery_app = Celery('worker')
celery_app.config_from_object(config)  # 把模块整体加载到app当中去
celery_app.autodiscover_tasks()





