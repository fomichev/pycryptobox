Overview
========

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

Features
--------

* Secure storage of sensitive information
* Desktop and mobile HTML pages for ease of use
* One-click login for sites without authenticity tokens (read more below)
* More-than-one-click login for sites with authenticity tokens (that still
saves you from manually copy-pasting your passwords)
* Really small amount of code. You can get through it probably within a hour
or two (to feel good that your data is safe)
* Works on every platform where you have browser (everywhere)

Guts
----

All information is stored in the `private/cryptobox` file,
encrypted via [AES](http://en.wikipedia.org/wiki/Advanced_Encryption_Standard);
key length is 256 bits and it is derived from your password using
[PBKDF2](http://en.wikipedia.org/wiki/Pbkdf2)
(consult your lawyer about whether it's considered crime in your country).
To check the integrity of the database, python code uses [HMAC-MD5](http://en.wikipedia.org/wiki/HMAC), while HTML page relies on specific magic field value in the
JSON data.

When `cbedit` generates HTML, it asks your password, decrypts
`private/cryptbox` file and merges it with JSON
patterns from `include/` directory (more on this later), encrypts it using
AES and puts this information into HTML page. Later on, when you
open it in the browser, it will ask your password and decrypt attached
database on the fly. So, your sensitive information is never exposed in
plain text.

The steps `cbedit` does are:

* Reads `private/cryptobox` and decrypts it
* For each type of entry in this file, reads appropriate JSON file from
`include/` and merges it with entry's variables (username, password, etc)
* Merges all JSON entries into one string and encrypts it with AES
* Embeds this encrypted data into pre-baked HTML page (look at `html/` for
more details)
* Embeds JavaScript and CSS (along with images) into HTML page and stores it
under `private/cryptobox/html` directory (cryptobox.html - is a desktop
version; m.cryptobox.html - is a mobile one)

If you're brave enough (or just want to understand what's going on under the
hood), you can enable debug mode in the `lib/cfg.py` file; after that,
all data from the aforementioned steps will be stored in the `private/tmp/`
directory. You can also change cipher parameters (e.g. PBKDF2 salt) and
entryped data file path in the `lib/cfg.py` file.

Bookmarklet
-----------

Some sites use authenticity token which they place into the HTML you get;
the login form along the username and password fields contains hidden field
with authenticity token. So it's no longer possible to use one-click login
feature with such sites. But there is a solution!

There is a bookmarklet that you can run on a login page; it will parse the form
data and will let you copy it in JSON format. Then, when you press 'Log in'
button for token based sites, you'll be asked for this data. After you paste it
and press 'OK' you'll be automatically logged in (using provided authenticity
token and your username/password).

When you're adding such form to the logins storage (`include/login`), you
should set token field value to `@token`; that will lead to pop-up dialog
box on login asking you to provide form data (you may have multiple tokens
within forms).

Required python modules
=======================

If your operation system of choice is Windows (sigh), then it's required to
have the following path in your PATH environment variable -
`c:\Python26\Scripts\` (assuming default python installation).

- Install pip

	$ easy_install pip

- Install [PBKDF2](https://www.dlitz.net/software/python-pbkdf2/)

	$ pip install pbkdf2

- Install [PyCrypto](https://www.dlitz.net/software/pycrypto/)

	$ pip install pycrypto

- Install [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/)

	$ pip install beautifulsoup4

- Install argparse (only for Python < 2.7)

	$ pip install argparse

Installation on Windows
-----------------------

Get python 2.6 and install all required modules from the previous section.
Also don't forget to add `c:\Python26\Scripts\` to your PATH environment
variable.

Installation on Mac OS X
------------------------

Use `brew` to get python 2.7 and then install required modules.

Installation on Linux
---------------------

Chances are, you'll already have python 2.6 or 2.7 on a Linux machine;
so just install the required modules.

Usage
=====

- Create database (creates empty `private/cryptobox` and
`private/cryptobox.hmac`)

	$ ./cbcreate

- Edit your database (it will also update html page at
`private/html/cryptobox.html` and at `private/html/m.cryptobox.html`)

	$ ./cbedit

Whenever you edit cryptobox database, the backup file (`private/cryptobox.tar`)
is created with the previous version of your database. So if some unexpected
error happens, you can always restore your previous database contents from
simple tar archive.

- Change password (every couple of months)

	$ ./cbpasswd

- Update HTML page (perform HTML page update without update to database - only for development)

	$ ./cbhtml

Database format
===============

Your sensitive information is stored in the form of entries; there may be a
number of entries, each describing particular login, bookmark, secure note or
other information.

Entry has the following structure (everything enclosed in [] is optional):

	<entry type>[@<entry tag>]:

		[variable1=value1]

		[variable2=value2]

		[variableN=valueN]

You don't need to quote anything; just put variable name on the left side of `=`
sign and variable value on the right side of `=` sign without any quotes. If you
want to have a multi line value, here document is supported (like in shell,
Perl, etc). You just put `<<SEPARATOR` in place of value and all the lines
from the next one until the line which contains only `SEPARATOR` is multi line
value (you can use any characters sequence instead of `SEPARATOR`).

Entry type is a relative path to a file inside the `include/` directory. And
the first component in this path (until the first `/` of end of string) will
form a tab in the HTML page. So, for example, if you have `login/google.com`
and `login/yahoo.com`, there will be a `Logins` page (or `login` if you don't
have translation for this page) in the HTML document
containing two entries. If you have several `note` entries, they will
be located on anther tab.

Each file in the `include/` directory is a JSON file which describes the
format and layout of entry. Variables from the entry will be substituted with
`$variableN` inside the JSON file and will form particular login/bookmark/etc.
There is some special handling for the login entries, where it's expected to
have `form` information with `$username` and `$password` variables.
For ther other entries, there will be probably only `text` variable that will
somehow format other variables from the entry.

Extending / Adding new login (includes)
---------------------------------------

I think it's pretty straightforward. You can use aforesaid bookmarklet on
your target site. The only caveat is that it can have multiple forms on one
page, so watch out and select the one you need (don't copy leading `[` and
trailing `]`, JSON data should start with `{` and end with `}`). Afterwards,
look through the JSON and place `$username` and `$password` into appropriate
form fields (look for other logins JSON data in `include/login`, it will
become clear from the example what to do).

Database example
----------------

	login/dropbox.com:
		username=qwe@qwe.qwe
		password=pwd

	login/gmail.com:
		username=qwe@qwe.qwe
		password=pwd

	card:
		name=bank
		cardholder=Jonh Smith
		number=1234 5678 9012 3456
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

	note:
		name=Multiline Note
		text=<<<YOUR_MARKER
	line1

	line2
	YOUR_MARKER

Import database
---------------

No, there is probably no easy way to automate it (taking into account the
number of existing formats); you have to create (or use pre-created) JSON
form layout in the `include/login` directory (vid provided bookmarklet)
and then add entry with your username/password to `private/cryptobox` manually.

I'm not telling its impossible; I just see no need to implement it myself.

Export database
---------------

No, there is no reasons to switch from cryptobox :-) But if you have strong
reasons, you can always implement `private/cryptobox` parser yourself; the
format is very easy to parse and all routines that decrypt data are waiting
for you in the `lib/` directory.

Works on (where it has been tested)
===================================

- Chrome 18, 19

- Firefox 11, 12

- Safari 5

- iPhone (iOS 5)

Used components
===============

Python
------

- [PBKDF2](http://www.dlitz.net/software/python-pbkdf2/) - MIT

- [AES](https://www.dlitz.net/software/pycrypto/) - Public Domain

- [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/) - Python

- [HMAC-MD5](http://docs.python.org/library/hmac.html) - Python

JavaScript
----------

- [PBKDF2, AES](https://code.google.com/p/crypto-js/) - New BSD License

	html/extern/CryptoJS (v3)

	html/extern/cjs (v2.5)

- [Random Seed](http://davidbau.com/archives/2010/01/30/random_seeds_coded_hints_and_quintillions.html) - BSD

	html/extern/seedrandom.js

	html/extern/seedrandom.min.js (via http://closure-compiler.appspot.com/home)


- [jQuery](http://jquery.com) - MIT

	html/extern/jquery

- [jQuery UI](http://jqueryui.com/download) - MIT

	html/extern/jquery-ui (Dialog, Tabs, Accordion, Button)

- [jQuery Mobile](http://jquerymobile.com) - MIT

	html/extern/jquery-mobile

- [Clippy](https://github.com/mojombo/clippy) - MIT

	html/extern/clippy

	private/html/clippy.swf
