def update(db_conf, password):
    include = (
            "html/extern/CryptoJS/components/core-min.js",
            "html/extern/CryptoJS/components/enc-base64-min.js",
            "html/extern/CryptoJS/components/cipher-core-min.js",
            "html/extern/CryptoJS/components/aes-min.js",
            "html/extern/CryptoJS/components/sha1-min.js",
            "html/extern/CryptoJS/components/hmac-min.js",
            "html/extern/CryptoJS/components/pbkdf2-min.js",

            "html/js/login.js",
            "html/js/view.js",
            "html/js/password.js",
            "html/js/crypto.js",
            "html/js/lock.js"
            )

    scripts = ""
    for s in include:
        scripts += open(s).read().decode('utf-8')

    print scripts

    pass
