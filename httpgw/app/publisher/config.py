import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    USERNAME = os.environ.get('USERNAME') or 'rabbitmq'
    PASSWORD = os.environ.get('PASSWORD') or 'rabbitmq'
    HOST = os.environ.get('HOST') or 'rabbitmq_rabbitmq_1'
    VHOST = os.environ.get('VHOST') or '/'
    EXCHANGE = os.environ.get('EXCHANGE') or 'message'
    EVENTRKEY = os.environ.get('EVENTRKEY') or 'event'
    SNAPSHOTRKEY = os.environ.get('SNAPSHOTRKEY') or 'snapshot'
    EVENTQUEUENAME = os.environ.get('EVENTQUEUENAME') or 'event_queue'
    SNAPSHOTQUEUENAME = os.environ.get('SNAPSHOTQUEUENAME') or 'snapshot_queue'
    DURABLE = os.environ.get('DURABLE') or True
    


