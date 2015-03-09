import os

DEBUG = True

BROKER_URL = 'amqp://{}:{}//'.format(
    os.environ.get('RABBITMQ_PORT_5672_TCP_ADDR', ''),
    os.environ.get('RABBITMQ_PORT_5672_TCP_PORT', ''),
)
CELERY_RESULT_BACKEND = 'amqp://{}:{}//'.format(
    os.environ.get('RABBITMQ_PORT_5672_TCP_ADDR', ''),
    os.environ.get('RABBITMQ_PORT_5672_TCP_PORT', ''),
)
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True

STORAGE_METHOD = 'disk'
ARCHIVE_DIRECTORY = 'archive/'

STORE_HTTP_TRANSACTIONS = False

NORMALIZED_PROCESSING = ['cassandra', 'elasticsearch']
RAW_PROCESSING = ['cassandra', 'elasticsearch']

# SENTRY_DSN = '...'

USE_FLUENTD = True
FLUENTD_ARGS = {
    'tag': 'app.scrapi',
    'host': os.environ.get('FLUENTD_PORT_24224_TCP_ADDR', ''),
    'port': int(os.environ.get('FLUENTD_PORT_24224_TCP_PORT', 24224)),
}

PROTOCOL = 'http'
VERIFY_SSL = True

PLOS_API_KEY = '...'

FRONTEND_KEYS = [
    u'description',
    u'contributors',
    u'tags',
    u'raw',
    u'title',
    u'id',
    u'source',
    u'dateUpdated',
]

ELASTIC_TIMEOUT = 10
ELASTIC_URI = '{}:{}'.format(
    os.environ.get('ELASTICSEARCH_PORT_9200_TCP_ADDR', ''),
    os.environ.get('ELASTICSEARCH_PORT_9200_TCP_PORT', ''),
)
ELASTIC_INDEX = 'share'

CASSANDRA_URI = ['{}'.format(
    os.environ.get('CASSANDRA_PORT_9042_TCP_ADDR', ''),
)]
CASSANDRA_KEYSPACE = 'scrapi'
