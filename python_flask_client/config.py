DEBUG = False
SECRET_KEY = 'SUPERSECRETKEYHIHI'

CLIENT_ID = 'YOUR_APPLICATIONS_CLIENT_ID'
CLIENT_SECRET = 'YOUR_APPLICATIONS_CLIENT_SECRET'

OAUTH_ENDPOINT_AUTHORIZE = 'https://lab.orderbird.com/oauth2/authorize/'
OAUTH_ENDPOINT_TOKEN = 'https://lab.orderbird.com/oauth2/token/'
OAUTH_ENDPOINT_REFRESH = OAUTH_ENDPOINT_TOKEN

OAUTHLIB_INSECURE_TRANSPORT = True

API_WHOAMI = 'https://lab.orderbird.com/v1/whoami'
