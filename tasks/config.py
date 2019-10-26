broker_url = 'redis://10.11.70.200:6379/3'
broker_pool_limit = 100  # broker 连接池，默认是10
task_serializer = 'pickle'

timezone = 'Asia/Shanghai'
accept_content = ['pickle','json']
worker_redirect_stdouts_level = 'INFO'

# 结果的配置
result_backend = 'redis://10.11.70.200:6379/3'
result_serializer = 'pickle'
result_expires = 3600   # 任务过期时间
result_cache_max = 10000   # 任务结果最大的缓存数量