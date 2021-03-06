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
* Really small amount of code. You can get through it probably within an hour
or two (to ensure that your data is safe)
* Works on every platform with modern browser (everywhere)

Guts
----
All information is stored in the `private/cryptobox` file,
encrypted via [AES](http://en.wikipedia.org/wiki/Advanced_Encryption_Standard);
key length is 256 bits and it is derived from your master password (recommend
way to generate it - [Diceware](http://world.std.com/~reinhold/diceware.html))
using [PBKDF2](http://en.wikipedia.org/wiki/Pbkdf2)
(consult your lawyer about whether it's considered crime in your country).
To check the integrity of the database, python code uses
[HMAC-MD5](http://en.wikipedia.org/wiki/HMAC), while HTML page relies on
specific magic field value in the JSON data.

When `cbedit` generates HTML, it asks your password, decrypts
`private/cryptbox` file and merges it with JSON
patterns from `include/` directory (more on this later), encrypts it using
AES and puts this information into HTML page. Later on, when you
open it in the browser, it will ask your password and decrypt attached
database on the fly. So, your sensitive information is never exposed in
plain text.

The steps `cbedit` does are:

* Reads `private/cryptobox` and decrypts it in memory
* For each type of entry in this file, reads appropriate JSON file from
`include/` and merges it with entry's variables (username, password, etc)
* Merges all JSON entries into one string and encrypts it with AES
* Embeds this encrypted data into pre-baked HTML page (look at `html/` for
more details)
* Embeds JavaScript and CSS (along with images) into HTML page and stores it
under `private/html` directory (cryptobox.html - is a desktop
version; m.cryptobox.html - is a mobile one)

If you're brave enough (or just want to understand what's going on under the
hood), you can enable debug mode in the `lib/config.py` file; after that,
all data from the aforementioned steps will be stored in the `private/tmp/`
directory.

Form bookmarklet
----------------
Some sites use authenticity token which they place into the HTML you get;
the login form along with username and password fields contains hidden field
with authenticity token. So it's no longer possible to use one-click login
feature with such sites (where one-click login feature is simple post request
with known username and password). But there is a solution!

There is a bookmarklet that you can run on a login page; it will parse the form
data and will let you copy it in JSON format. Then, when you press 'Log in'
button for token based sites, you'll be asked for this data. After you paste it
and press 'OK' you'll be automatically logged in (using provided authenticity
token and your username/password).

When you're adding such form to the logins storage (`include/login`), you
should set token field value to `__token__`; that will lead to pop-up dialog
box on login asking you to provide form data (you may have multiple tokens
within forms).

TODO: Describe how to get this bookmark; also describe login bookmark.

	javascript:(function(){s=document.createElement('SCRIPT');s.type='text/javascript';s.src='https://<BOOKMARKLET_PATH>';document.getElementsByTagName('head')[0].appendChild(s);})();

Fill bookmarklet
----------------
T.b.d

Required python modules
=======================
Python version 2.6 or 2.7 required!

If your operation system of choice is Windows (sigh), then it's required to
have the following path in your PATH environment variable -
`c:\Python26\Scripts\` (assuming default python installation).

* Install pip

	$ easy_install pip

* Install [PBKDF2](https://www.dlitz.net/software/python-pbkdf2/)

	$ pip install pbkdf2

* Install [PyCrypto](https://www.dlitz.net/software/pycrypto/)

	$ pip install pycrypto

* Install argparse (only for Python < 2.7)

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
* Create database (creates empty `private/cryptobox` and
`private/cryptobox.hmac`)

	$ ./cbcreate

Upon database creation, PBKDB2 salt and AES IV will be generated. That
guarantees that even two databases with equal content will be encrypted to
different cipher text.

* Edit your database (it will also update html page at
`private/html/cryptobox.html` and at `private/html/m.cryptobox.html`)

	$ ./cbedit

Whenever you edit cryptobox database, the backup file (`private/cryptobox.tar`)
is created with the previous version of your database. So if some unexpected
error happens, you can always restore your previous database contents from
simple tar archive.

* Change password (every couple of months)

	$ ./cbpasswd

As in `cbedit` command, backup file will be created (or updated) whenever
you change the password.

Database format
===============
Windows INI-like file format is used for database (on Linux it normally has
.conf extension). More information with examples can be found in the
[appropriate python page](http://docs.python.org/library/configparser.html).

Your sensitive information is stored in the form of entries; there may be a
number of entries, each describing particular login, bookmark, secure note or
other information.

Entry has the following structure:

	[<entry type>  <entry name>]
	tag=<tag>

	hidden=yes

	<variable1>=<value1>

	<variableN>=<valueN>

	<multiline>:<line1>
	            <line2>

You don't need to quote anything; just put variable name on the left side of `=`
sign and variable value on the right side of `=` sign without any quotes. If you
want to have a multi line value, use colon (:) to delimit variable name from
value and follow the example above.

Entry type is a relative path to a file inside the `include/` directory. And
the first component in this path (until the first `/` of end of string) will
form a tab in the HTML page. So, for example, if you have `login/google.com`
and `login/yahoo.com`, there will be a `login` page (or `Logins` because of
pre-defined translations) in the HTML document
containing two entries. If you have several `note` entries, they will
be located on anther tab. Be aware that you can't have two entries with the
same `entry type` and `entry name`!

Each file in the `include/` directory is a JSON file which describes the
format and layout of entry. Variables from the entry will be substituted with
`@variableN@` inside the JSON file and will form particular login/bookmark/etc.
There is some special handling for the login entries, where it's expected to
have `form` information with `@name@` and `@password@` variables.
For the other entries, there will be probably only `text` variable that will
somehow format other variables from the entry.

Entry name has special meaning for login entry type: it should contain your
username. For the other entry types, entry name is just the caption of
the entry.

Tag variable will let you 'merge' several entries into a block (they will
be placed close to each other on the HTML page). You don't have to
use tag variable, it's usage is optional (and intended to help you with
the clutter).

You can use `hidden=yes` to remove some entries from the final HTML page (this
is handy for the entries you want to keep and be able to access at some point
but don't want it to clutter your HTML).

Comments are started with `#` and ended at the end of the line.

Extending / Adding new login (includes)
---------------------------------------
I think it's pretty straightforward. You can use aforesaid `form` bookmarklet
on your target site. The only caveat is that it can have multiple forms on one
page, so watch out and select the one you need (don't copy leading `[` and
trailing `]`, JSON data should start with `{` and end with `}`). Afterwards,
look through the JSON and place `@name@` and `@password@` into appropriate
form fields (look for other logins JSON data in `include/login`, it will
become clear from the example what to do). Better yet, you can fill in the
form in the browser with `@name@` and `@password@` and run the bookmarklet;
this way, you don't need to dig into the JSON and find out were to put
these marks, they will already be in place.

Database example
----------------

	[login/dropbox.com qwe@qwe.qwe]
	password=pwd

	[login/gmail.com qwe@qwe.qwe]
	password=pwd

	[card bank]
	cardholder=Jonh Smith
	number=1234 5678 9012 3456
	pin=1234
	cvv=123

	[note note]
	text=with body

	[app Photoshop]
	key=secret

	[bookmark Google]
	url=http://google.com
	comment=Google search

	[note Multiline Note]
	text:line1
	     line2

Import database from other password managers
--------------------------------------------
No, there is probably no easy way to automate it (taking into account the
number of existing formats); you have to create (or use pre-created) JSON
form layout in the `include/login` directory (via provided bookmarklet)
and then add entry with your username/password to `private/cryptobox` manually.

I'm not telling its impossible; I just see no need to implement it myself.

Export database
---------------
No, there are no reasons to switch from cryptobox :-) But if you have strong
reasons, you can always implement `private/cryptobox` parser yourself; the
format is pretty simple to parse (there are probably available implementations
for languages other that Python) and all routines that decrypt data are waiting
for you in the `lib/` directory.

Configuration
=============
You can configure cryptobox via configuration file called `.cryptoboxrc`.
When you run any of the cryptobox commands, it first searches for the
`.cryptoboxrc` file in the current directory, then it tries to find this
file in your home directory, and if it didn't find any configuration, it
will use the default one. You can also pass configuration file path to
the tools via `-c` command line option.

Configuration file is simple INI-like file with the following
possible variables:

	[path]
	db = <path to cryptobox database directory>
	db_bookmarklet_login = <where to store login bookmarklet>
	db_bookmarklet_form = <where to store form bookmarklet>

	[ui]
	jquery_ui_theme = <use different jquery-ui theme>
	editor = <full path to your editor>
	lang = <select language; currently supported are en and ru>

	[security]
	lock_timeout_minutes = <web site lock timeout in minutes>
	default_password_length = <default password length in generate dialog>

All the options are optional. You can dig default values in
the `lib/cfg.py` file.

Works on (where it has been tested)
===================================
* Chrome 18, 19, 20

* Firefox 11, 12

* Safari 5

* Chrome Beta (Android 4)

* iPhone (iOS 5)

Used components
===============

Python
------
* [PBKDF2](http://www.dlitz.net/software/python-pbkdf2/) - MIT

* [AES](https://www.dlitz.net/software/pycrypto/) - Public Domain

* [HMAC-MD5](http://docs.python.org/library/hmac.html) - Python

* [Mozilla preprocessor](http://mxr.mozilla.org/mozilla-central/source/config/) - Mozilla Public License 2

	lib/extern/Expression.py f4157e8c4107

	lib/extern/Preprocessor.py 13ea641e1b5a

JavaScript
----------
* [CryptoJS 3.0.2](https://code.google.com/p/crypto-js/) - New BSD License

	html/extern/CryptoJS

* [Random Seed 2.0](http://davidbau.com/archives/2010/01/30/random_seeds_coded_hints_and_quintillions.html) - BSD

	html/extern/seedrandom.js

	html/extern/seedrandom.min.js (via http://closure-compiler.appspot.com/home)

* [jQuery 1.7.2](http://jquery.com) - MIT

	html/extern/jquery

* [jQuery UI 1.8.21](http://jqueryui.com/download) - MIT

	html/extern/jquery-ui (Dialog, Tabs, Accordion, Button, Flick theme)

* [jQuery Mobile 1.1.0](http://jquerymobile.com) - MIT

	html/extern/jquery-mobile

* [Clippy 7329b72360](https://github.com/mojombo/clippy) - MIT

	html/extern/clippy

	private/html/clippy.swf

Decrypt data without cryptobox
==============================
Even if you don't have cryptobox available, you may still fairly easy
decrypt your data.

Lets suppose, you have the following data encrypted:

	[login/dropbox.com your_username]
	password=your_password

With the following contents of `cryptobox.conf` file:

	[pbkdf2]
	salt_len = 8
	salt = vyvhYAqR0Os=
	iterations = 1000

	[aes]
	iv_len = 16
	bs = 32
	iv = O/fqt3VeY4laxfn1B7OyHQ==

	[cryptobox]
	format_version = 2

You get the following cipher text:

	$ cat cryptobox
	JhDP/N2YSG54jHmJgqPqVcWRCh6VoRMqaxq3SzEoFdUwdwm9wIm9ec8DSzTf7NiNEeHTEYZsNjAp
	wSuPGIiTkA==

Now, let's try to decrypt it (instruction provided for Linux)!

Before you proceed, I want to warn you that the following commands are not
safe! You will pass your AES key to the `openssl` utility via command line
(and will also store your plaintext password in the file). So make it if
you really need to get your data no matter what consequences may be.
The following text is used just to demonstrate that your data could be
easily decrypted using standard tools.

Give me the key!
----------------
You have to take out the value of pbkdf2.salt field of config and convert
it to hex enconding:

	$ echo "vyvhYAqR0Os=" | base64 -d | xxd -ps
	bf2be1600a91d0eb

Next, go and download a Perl script which implements PBKDF2 using OpenSSL:

	$ wget http://www.ict.griffith.edu.au/anthony/software/pbkdf2.pl

Store your password in `pwd` file and execute Perl script (where 1000 is the
pbkdf2.iterations from config):

	$ cat pwd
	hi

	$ perl pbkdf2.pl bf2be1600a91d0eb 1000 < pwd > result

	$ cat result
	0bd89afa21176ec9943aa5ae6a146b58a17901e50e8e6b0ab66fc12c7e094d9df7f3405ab410f4bf431e0bb560495e87

And because we are interested only if first 32 bytes, we need to cut the rest
(the number 64 in the following command is 32 * 2 because each byte in hex
encoding is represented by two characters)

	$ cat result | cut -b1-64 > secret
	$ cat secret
	0bd89afa21176ec9943aa5ae6a146b58a17901e50e8e6b0ab66fc12c7e094d9d

Decrypt my data
---------------
Now, we have a key, the only thing we need to do is to convert initialization
vector (aes.iv) to hex and call openssl, let's do it:

	$ echo "O/fqt3VeY4laxfn1B7OyHQ==" | base64 -d | xxd -ps
	3bf7eab7755e63895ac5f9f507b3b21d

	$ openssl enc -d -aes-256-cbc -K 0bd89afa21176ec9943aa5ae6a146b58a17901e50e8e6b0ab66fc12c7e094d9d -iv 3bf7eab7755e63895ac5f9f507b3b21d -base64 -in cryptobox -out plaintext

	$ cat plaintext
	[login/dropbox.com your_username]
	password=your_password$

Congratulations, plaintext contains decrypted content of your cryptobox. Now,
it's better to remove all temporary files and clean `bash` history.

TODO: describe the following features
=====================================
* broken logins
* comments in include/ JSON
* cryptobox.json
