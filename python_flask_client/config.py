DEBUG = False
SECRET_KEY = 'SUPERSECRETKEYHIHI'

CLIENT_ID = 'YOUR_APPLICATIONS_CLIENT_ID'
CLIENT_SECRET = 'YOUR_APPLICATIONS_CLIENT_SECRET'

OAUTH_ENDPOINT_AUTHORIZE = 'https://sandbox-myob.orderbird.com/oauth2/authorize/'
OAUTH_ENDPOINT_TOKEN = 'https://sandbox-myob.orderbird.com/oauth2/token/'
OAUTH_ENDPOINT_REVOKE = 'https://sandbox-myob.orderbird.com/oauth2/revoke_token/'
OAUTH_ENDPOINT_REFRESH = OAUTH_ENDPOINT_TOKEN

OAUTHLIB_INSECURE_TRANSPORT = True

API_WHOAMI = 'https://sandbox-api.orderbird.com/public/v1/whoami'
