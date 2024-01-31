origins = ['http://localhost:44000', 'http://192.168.1.115:44000']
db_broker = 'redis://localhost:6379'
const = ['http://192.168.1.113:54515/api/', 'http://d1130e4458f2.sn.mynetname.net:13901']

# celery -A src.operations.async_request:celery_manager worker --loglevel=INFO --pool=solo
# celery -A src.operations.async_request:celery_manager flower
