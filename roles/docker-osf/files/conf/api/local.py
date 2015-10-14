from . import defaults

API_BASE = 'v2/'
#SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')  # necessary when offloading ssl
STATIC_URL = '/{}static/'.format(API_BASE)
SWAGGER_SETTINGS = dict(defaults.SWAGGER_SETTINGS, base_path='test-api.osf.io/v2/docs')
