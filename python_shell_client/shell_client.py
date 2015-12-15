import logging

from requests_oauthlib import OAuth2Session

logging.basicConfig(level=logging.DEBUG)

CLIENT_ID = 'INSERT_YOUR_CLIENT_ID_HERE'
CLIENT_SECRET = 'INSERT_YOUR_CLIENT_SECRET_HERE'
SERVER_URL = 'https://lab.orderbird.com'

redirect_uri = 'http://localhost:5000/authorized/'
scope = ['account-read']

authorization_base_url = SERVER_URL + '/oauth2/authorize/'
token_url = SERVER_URL + '/oauth2/token/'

myob_oauth = OAuth2Session(CLIENT_ID,
                           scope=scope,
                           redirect_uri=redirect_uri)

# Redirect user to my.orderbird to get authorization
authorization_url, state = myob_oauth.authorization_url(
    authorization_base_url,
)
print 'Please go here and authorize,', authorization_url

# Get the authorization verifier code from the callback url
redirect_response = raw_input('Paste the full redirect URL here:')

# Fetch the access token
myob_oauth.fetch_token(token_url,
                       client_secret=CLIENT_SECRET,
                       authorization_response=redirect_response)

# Fetch a protected resource, i.e. whoami
r = myob_oauth.get(SERVER_URL + '/v1/whoami/')
print r.content
