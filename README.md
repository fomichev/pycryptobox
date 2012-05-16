# Overview

Cryptobox is a bunch of python scripts that will help you manage your
passwords database. The idea is simple: you have some encrypted file
(`private/cryptobox`) where you store your sensitive information. To edit
it you use special script (`cbedit`) which will open your favorite editor
and let you update passwords/bookmarks/notes/etc. When the editor is
closed, `cbedit` will create beautiful and easy to navigate HTML page with
all your sensitive information (encrypted). This HTML page will also
contain JavaScript code which can decrypt your data when given correct
password.

... go on ...

## Guts

Your sensitive information is stored in the `private/cryptobox` file,
encrypted via AES; key is derived from your password using PBKDF2.

When `cbedit` generates HTML, it asks your password, decrypts
`private/cryptbox`file and merges it with JSON
patterns from `include/` directory (more on this later), encrypts it using
AES/PBKDF2 and puts this information into HTML page. Later on, when you
open it in the browser, it will ask your password and decrypt attached
database on the fly. So, your sensitive information is never exposed in
plain text.

... go on ...


## Extending / Adding new login (includes)

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

## Installation on Windows

t.b.d.

## Installation on Mac OS X

t.b.d.

## Installation on Linux

t.b.d.

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

	html/extern/seedrandom.min.js (via http://closure-compiler.appspot.com/home)


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

	Logins/dropbox.com:
		username=qwe@qwe.qwe
		password=pwd

	Logins/gmail.com:
		username=qwe@qwe.qwe
		password=pwd

	Cards:
		name=bank
		cardholder=Jonh Smith
		number=1234 5678 9012 3456
		pin=1234
		cvv=123

	Notes:
		name=note
		text=with body

	Applications:
		name=Photoshop
		key=secret

	Bookmarks:
		name=Google
		url=http://google.com

	Notes:
		name=Multiline Note
		text=<<<YOUR_MARKER
	line1

	line2
	YOUR_MARKER

# Works on (where it has been tested)

- Chrome 18

- Safari 5

- Firefox 11, 12

- iPhone (iOS 5)
