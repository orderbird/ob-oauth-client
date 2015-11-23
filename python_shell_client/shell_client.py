import logging

from requests_oauthlib import OAuth2Session

logging.basicConfig(level=logging.DEBUG)

CLIENT_ID = 'mmBkMZM5El0RVbhAJEWSE1W5R8oOkEL8V9mKeKhp'
CLIENT_SECRET = '14qlnQe0BadwF9DkEmBgmQExlYmPkxaZ5mGGsDkY3KRG4OPuj0VX4xvQTpR6axXAE1gfRWAojL4MQQTMO7XODDorCe64PSplIr4JrhHEMFB69KIOeaARKEElfZQIUdPF'
SERVER_URL = 'https://lab.orderbird.com/'

redirect_uri = 'http://localhost:5000/authorized/'
scope = ['read', 'account']

authorization_base_url = SERVER_URL + '/oauth2/authorize/'
token_url = SERVER_URL + '/oauth2/token/'

myob_oauth = OAuth2Session(CLIENT_ID,
                           scope=scope,
                           redirect_uri=redirect_uri)

# Redirect user to my.orderbird to get authorization
authorization_url, state = myob_oauth.authorization_url(
    authorization_base_url,
    access_type='offline',
    approval_prompt='force'
)
print 'Please go here and authorize,', authorization_url

# Get the authorization verifier code from the callback url
redirect_response = raw_input('Paste the full redirect URL here:')

# Fetch the access token
myob_oauth.fetch_token(token_url,
                       client_secret=CLIENT_SECRET,
                       authorization_response=redirect_response)

# Fetch a protected resource, i.e. whoami
r = myob_oauth.get(SERVER_URL + '/api/v3/whoami/')
print r.content
