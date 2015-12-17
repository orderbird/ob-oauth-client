<?php

# Replace this value with the path to the Unirest PHP library
require_once 'lib/unirest-php-master/src/Unirest.php';

# Your application's ID and secret
$applicationId = 'REPLACE_ME';
$applicationSecret = 'REPLACE_ME';
$redirectUri = 'http://localhost/callback.php';

$connectHost = 'https://lab.orderbird.com';

# Headers to provide to OAuth API endpoints
$oauthRequestHeaders = array (
  'Authorization' => 'Client ' . $applicationSecret,
  'Accept' => 'application/json',
  'Content-Type' => 'application/x-www-form-urlencoded'
);

# Serves requests from orderbird to your application's redirect URL
# Note that you need to set your application's Redirect URL
function callback() {
  global $applicationId, $applicationSecret, $redirectUri;
  global $connectHost, $oauthRequestHeaders;

  # Extract the returned authorization code from the URL
  $authorizationCode = $_GET['code'];
  if ($authorizationCode) {

   ## Provide the code in a request to the Obtain Token endpoint
    $oauthRequestBody = array(
      'grant_type' => 'authorization_code',
      'code' => $authorizationCode,
      'client_id' => $applicationId,
      'client_secret' => $applicationSecret,
      'redirect_uri' => $redirectUri
    );
    $oauthRequestBodyEnc = http_build_query($oauthRequestBody);

    $response = Unirest\Request::post($connectHost . '/oauth2/token/', $oauthRequestHeaders, $oauthRequestBodyEnc);

    # Extract the returned access token from the response body
    if (property_exists($response->body, 'access_token')) {

      # Here, instead of printing the access token, your application server should store it securely
      # and use it in subsequent requests to the Connect API on behalf of the merchant.
      echo '<br>Access token: ' . $response->body->access_token;
      echo '<br>Authorization succeeded!';

      # The response from the Obtain Token endpoint did not include an access token. Something went wrong.
    } else {
      echo '<br>Code exchange failed!';
    }

    # The request to the Redirect URL did not include an authorization code. Something went wrong.
  } else {
    echo '<br>Authorization failed!';
  }
}

# Execute the callback
callback();

?>
