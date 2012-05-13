function decrypt(pass, salt, cipher) {
	var pbk = Crypto.PBKDF2(pass, salt, 32, { iterations: 1000 });
	var secret = Crypto.util.hexToBytes(pbk);
	var text = Crypto.util.base64ToBytes(cipher);

	return Crypto.AES.decrypt(text, secret, { mode: new Crypto.mode.CFB });
}

function unlock(pwd) {
	var text=decrypt(pwd, _cfg_salt, _cfg_cipher);

	document.getElementById("cipher").innerHTML=text;

	var data = eval(text);

	var text = "";
	for (var i = 0; i < data.length; i++) {
		var el = data[i];
		var link = createLink(el.name, el.address, el.form);

		var showUsername = createHiddenOnClick("Show username", el.vars.username);
		var showPassword = createHiddenOnClick("Show password", el.vars.password);
		var showJson = createHiddenOnClick("Show JSON", JSON.stringify(el));

		text += '<h1>' + link + '</h1>';
		text += '<p>' + showUsername + '</p>';
		text += '<p>' + showPassword + '</p>';
		text += '<p>' + showJson + '</p>';
	}

	document.getElementById("links").innerHTML=text;
}

function lock() {
	document.getElementById("cipher").innerHTML="";
	document.getElementById("links").innerHTML="";
}
