# Overview

Cryptobox is a bunch of python scripts that will help you manage your
passwords database and other sensitive data. The idea is simple: there is
some encrypted file (`private/cryptobox`) where sensitive information is
stored. To edit it you use special script (`cbedit`) which will open editor
and let you update passwords/bookmarks/notes/etc. When the editor is
closed, `cbedit` will create beautiful and easy to navigate HTML page with
all your sensitive information (encrypted). This HTML page will also
contain JavaScript code which can decrypt attached encrypted data on the fly
when given correct password.

Your sensitive information is never exposed; it's never stored on the disk
in the plain text and exists in the HTML page only in the encrypted form.

## Features:

* Secure storage for sensitive information
* Desktop and mobile HTML pages for ease of use
* One-click login for sites without authenticity tokens (read more below)
* More-that-one-click login for sites with authenticity tokens (that still saves you from manually copy-pasting your passwords)
* Really small amount of code. You can get through it probably within a day (to feel good that your data is safe)

## Guts

All information is stored in the `private/cryptobox` file,
encrypted via AES; key length is 265 bits and it is derived from your password
using PBKDF2 (consult your lawyer whether is considered crime in your country).

When `cbedit` generates HTML, it asks your password, decrypts
`private/cryptbox` file and merges it with JSON
patterns from `include/` directory (more on this later), encrypts it using
AES and puts this information into HTML page. Later on, when you
open it in the browser, it will ask your password and decrypt attached
database on the fly. So, your sensitive information is never exposed in
plain text.

The steps are:

* Read `private/cryptobox` and decrypt it
* For each type of entry in this file, read appropriate JSON file from `include/` and merge it with entry's variables (username, password, etc)
* Merge all JSON entries into one string and encrypt it with AES
* Embed this encrypted data into pre-baked HTML page (look at `html/` for more details)
* Embed JavaScript and CSS (along with images) into HTML page and store it under `private/cryptobox/html` directory (cryptobox.html - is a desktop version; m.cryptobox.html - is a mobile one)

If you're brave enough (or just want to understand what's going on under the
hood), you can enable debug mode in the `lib/cfg.py` file; after that,
all data from the aforementioned steps will be stored in the `private/tmp/`
directory. There you can also change cipher parameters (e.g. PBKDF2 salt).

## Bookmarklet

Some sites use authenticity token which they place into the HTML you get;
the login form along the username and password fields contains hidden field
with authenticity token. So it's no longer possible to use one-click login
feature with such sites. But there is a solution!

There is a bookmarklet that you can run on a login page; it will parse the form
data and will let you copy it in JSON format. Then, when you press 'Log in'
button for token based sites, you'll be asked this data. After you paste it
and press 'OK' you'll be automatically logged in (using provided authenticity
token).

## Extending / Adding new login (includes)

I think it's pretty straightforward. You can use aforesaid bookmarklet on
your target site. The only caveat is that it can have multiple forms on one
page, so watch out and select the one you need. Afterwards, look through the
JSON and place $username and $password into appropriate form fields (look
for other logins JSON data in `include/Logins`, it will become clear from
the example what to do).

# Required python modules:

If your operation system of choice is Windows (sigh), then it's required to
have the following path in your PATH environment variable -
c:\Python26\Scripts\ (assuming default python installation).

- install pip

	$ easy_install pip

- install https://www.dlitz.net/software/python-pbkdf2/

	$ pip install pbkdf2

- install https://www.dlitz.net/software/pycrypto/

	$ pip install pycrypto

- install http://www.crummy.com/software/BeautifulSoup/

	$ pip install beautifulsoup4

## Installation on Windows

Get python 2.6 and install all required modules from the previous section.
Also don't forget to add 'c:\Python26\Scripts\' to your PATH environment
variable.

## Installation on Mac OS X

Use `brew` to get python 2.7 and then install required modules.

## Installation on Linux

You'll already have python 2.6 or 2.7 on a linux machine; just install the
required modules.

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
