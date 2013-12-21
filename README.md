Bitcasa SDK for Python
===============

Bitcasa SDK for Python, providing access to Bitcasa's REST API.

License: MIT

Requirements:
* requests >= 1.2.3

Setup
===============
Install bitcasa library
```
pip install bitcasa
```

Get A Bitcasa Developer API Key
===============
In order to access the API successfully, you need to first get an API key from Bitcasa.
* Go to: [https://developer.bitcasa.com/](https://developer.bitcasa.com/)
* Either sign up with your Bitcasa account, or log in with it
* Click "Console" on the top header, and "Create App" on the top right
* Save your Client ID and your Client Secret locally; you will use them in your code


Using The Bitcasa API
===============
In order to access a Bitcasa user's files, you'll need to do authorize your application with the user via our authentication exchange. Once completed, you'll gain an access token that you can utilize for API usage.

Examine the tests for examples of usage.
