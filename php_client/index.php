<?php

  # This file simply serves the link that merchants click to authorize your application.
  # When authorization completes, a notification is sent to your redirect URL, which should
  # be handled in callback.php.

  $applicationId = 'REPLACE_ME';
  $redirectUri = 'http://localhost/callback.php';
  $scope = 'account-read';

  echo "<a href=\"https://lab.orderbird.com/oauth2/authorize/?response_type=code&client_id=$applicationId&redirect_uri=$redirectUri&scope=$scope&access_type=offline&approval_prompt=force\">Click here</a> to authorize the application.";
?>
