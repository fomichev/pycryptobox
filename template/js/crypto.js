function decrypt(pass, salt, cipher) {
	var pbk = Crypto.PBKDF2(pass, salt, 32, { iterations: 1000 });
	var secret = Crypto.util.hexToBytes(pbk);
	var text = Crypto.util.base64ToBytes(cipher);

	return Crypto.AES.decrypt(text, secret, { mode: new Crypto.mode.CFB });
}

function unlock(pwd) {
	var text = decrypt(pwd, _cfg_salt, _cfg_cipher);
	var data = eval(text);
	text = "";

	var site = "";
	var app = "";
	var bookmark = "";
	var card = "";
	var note = "";


	for (var i = 0; i < data.length; i++) {
		var el = data[i];

		if (el.type == 'site') {
			site += createLink(el.name, el.address, el.form, el.vars.username, el.vars.password);
		} else if (el.type == 'app') {
			app += createApp(el.name, el.data.key);
		} else if (el.type == 'bookmark') {
			bookmark += createBookmark(el.name, el.data.url);
		} else if (el.type == 'card') {
			card += createCard(el.name, el.data.cardholder, el.data.cvv2, el.data.number, el.data.pin);
		} else if (el.type == 'note') {
			note += createNote(el.name, el.data.text);
		}
	}

	document.getElementById("site").innerHTML = site;
	document.getElementById("app").innerHTML = app;
	document.getElementById("bookmark").innerHTML = bookmark;
	document.getElementById("card").innerHTML = card;
	document.getElementById("note").innerHTML = note;

	document.getElementById("plaintext").innerHTML = createHiddenOnClick("JSON", text);
}

function lock() {
	document.getElementById("site").innerHTML = "";
	document.getElementById("app").innerHTML = "";
	document.getElementById("bookmark").innerHTML = "";
	document.getElementById("card").innerHTML = "";
	document.getElementById("note").innerHTML = "";

	document.getElementById("plaintext").innerHTML = "";
}
