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

- create database

	$ ./create_db

- edit your database

	$ ./edit_db

- change password

	$ ./password_db

- update html page

	$ ./update_html

# Used components

## Python

- PBKDF2 http://www.dlitz.net/software/python-pbkdf2/ (MIT)

- AES https://www.dlitz.net/software/pycrypto/ (Public Domain)

- HMAC (MD5)

## JavaScript

- PBKDF2, AES https://code.google.com/p/crypto-js/ (New BSD License)

	template/js/CryptoJS

	template/js/cjs

- Random Seed http://davidbau.com/archives/2010/01/30/random_seeds_coded_hints_and_quintillions.html (BSD)

	template/js/seedrandom.js

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
