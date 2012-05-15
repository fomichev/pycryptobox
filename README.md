# Overview

TODO: Put some info about architecture here...

## Bookmarklets

TODO: Describe why and what they do...

# Required python modules:

- install pip

	$ easy_install pip

- install https://www.dlitz.net/software/python-pbkdf2/

	$ pip install pbkdf2

- install https://www.dlitz.net/software/pycrypto/

	$ pip install pycrypto

- install http://www.crummy.com/software/BeautifulSoup/

	$ pip install beautifulsoup4

# Usage

- create database (creates empty private/cryptobox and private/cryptobox.hmac)

	$ ./cbcreate

- edit your database (it will also update html page at private/html/cryptobox.html and at private/html/m.cryptobox.html)

	$ ./cbedit

- change password (every couple of months)

	$ ./cbpasswd

- update html page (perform html page update without update to database - only for development)

	$ ./cbhtml

# Used components

## Python

- PBKDF2 http://www.dlitz.net/software/python-pbkdf2/ (MIT)

- AES https://www.dlitz.net/software/pycrypto/ (Public Domain)

- HMAC - MD5 (Python builtin)

## JavaScript

- PBKDF2, AES https://code.google.com/p/crypto-js/ (New BSD License)

	html/extern/CryptoJS (v3)

	html/extern/cjs (v2.5)

- Random Seed http://davidbau.com/archives/2010/01/30/random_seeds_coded_hints_and_quintillions.html (BSD)

	html/extern/seedrandom.js

- jQuery http://jquery.com (MIT)

	html/extern/jquery

- jQuery UI http://jqueryui.com/download (MIT)

	html/extern/jquery-ui (Dialog, Tabs, Accordion, Button)

- jQuery Mobile http://jquerymobile.com (MIT)

	html/extern/jquery-mobile


- Clippy https://github.com/mojombo/clippy (MIT)

	html/extern/clippy

	private/html/clippy.swf


# Database example

	site/dropbox.com:
		username=qwe@qwe.qwe
		password=pwd

	site/gmail.com:
		username=qwe@qwe.qwe
		password=pwd

	card:
		name=bank
		cardholder=Jonh Smith
		n=1234 5678 9012 3456
		pin=1234
		cvv=123

	note:
		name=note
		text=with body

	app:
		name=Photoshop
		key=secret

	bookmark:
		name=Google
		url=http://google.com

# Works on (where it has been tested)

- Chrome 18

- Safari

- Firefox 11, 12

- iPhone (iOS 5)
