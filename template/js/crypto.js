function decrypt(pass, salt, cipher) {
	var pbk = Crypto.PBKDF2(pass, salt, 32, { iterations: 1000 });
	var secret = Crypto.util.hexToBytes(pbk);
	var text = Crypto.util.base64ToBytes(cipher);

	return Crypto.AES.decrypt(text, secret, { mode: new Crypto.mode.CFB });
}

function unlock(pwd) {
	var text=decrypt(pwd, _cfg_salt, _cfg_cipher);

	document.getElementById("cipher").innerHTML=createHiddenOnClick("JSON", text);

	var data = eval(text);

	var text = "";
	for (var i = 0; i < data.length; i++) {
		var el = data[i];

		if (el.type == 'site') {
			text += createLink(el.name, el.address, el.form, el.vars.username, el.vars.password);
		} else if (el.type == 'card') {
			text += createCard(el.name, el.data.cardholder, el.data.cvv2, el.data.number, el.data.pin);
		} else if (el.type == 'note') {
			text += createNote(el.name, el.data.text);
		}
	}

	document.getElementById("links").innerHTML=text;
}

function lock() {
	document.getElementById("cipher").innerHTML="";
	document.getElementById("links").innerHTML="";
}
