function accordionItem(header, body) {
	return '<h3><a href="#">' + header + '</a></h3><div>' + body + '</div>';
}

function createLink(name, address, form, username, password) {
	var hocid = 0;
	function createHiddenOnClick(name, value) {
		return '<div class="expand"><strong>' + name + '</strong> (click to expand/collapse)</div><div>' + value + '</div>';
	}

	function withToken(form) {
		for (var key in form.fields) {
			var value = form.fields[key];

			if (value == "@token")
				return key;
		}

		return "";
	}

	var url = form.action;
	var title = name + " (" + username + ")"

	var k = "";
	var v = "";

	var r = "";

	for (var key in form.fields) {
		if (form.fields[key] == "@token")
			continue;

		if (k == "") {
			k = "new Array(\"" + key +"\"";
			v = "new Array(\"" + form.fields[key] +"\"";
		} else {
			k += ", \"" + key +"\"";
			v += ", \"" + form.fields[key] +"\"";
		}
	}
	k += ")"
	v += ")"


	var token = withToken(form);
	if (token != "") {
		r += '<a class="button-token" href="' + address + '" target="_blank">Get token</a>';
		r += '<a class="button-login" href="#" onClick=\'javascript:loginWithToken("' + url + '", "' + name + '", ' + k + ', ' + v + ', "' + token + '"); return false;\'>Login</a>';
	} else {
		r += '<a class="button-login" href="#" onClick=\'javascript:login("' + form.method + '", "' + url + '", "' + name + '", ' + k + ', ' + v + '); return false;\'>Login</a>';

	}


	r += '<a class="button-goto" href="' + address + '" target="_blank">Go to site</a>';
	r += '<p>' + createHiddenOnClick("Username", username) + '</p>';
	r += '<p>' + createHiddenOnClick("Password", password) + '</p>';

	return accordionItem(title, r);
}

function createApp(name, key) {
	return accordionItem(name, key);
}

function createBookmark(name, url, comment) {
	return accordionItem(name, '<a class="button-goto" href="' + url + '" target="_blank">Go to site</a><p>' + comment + '</p>');
}

function createCard(name, cardholder, cvv2, number, pin) {
	var d = "";
	d += "<p>Cardholder=" + cardholder + "</p>";
	d += "<p>Number=" + number + "</p>";
	d += "<p>CVV2=" + cvv2 + "</p>";
	d += "<p>PIN=" + pin + "</p>";

	return accordionItem(name, d);
}

function createNote(name, text) {
	return accordionItem(name, text);
}

function accordion(text) {
	return '<div class="accordion">' + text + '</div>';
}

function unlock(pwd) {
	var text = decrypt(pwd, _cfg_salt, _cfg_cipher);
	var data = eval(text);
	var map = {};

	map.site = "";
	map.app = "";
	map.bookmark = "";
	map.card = "";
	map.note = "";

	for (var i = 0; i < data.length; i++) {
		var el = data[i];

		if (el.type == 'site') {
			map.site += createLink(el.name, el.address, el.form, el.vars.username, el.vars.password);
		} else if (el.type == 'app') {
			map.app += createApp(el.name, el.data.key);
		} else if (el.type == 'bookmark') {
			map.bookmark += createBookmark(el.name, el.data.url, el.data.comment);
		} else if (el.type == 'card') {
			map.card += createCard(el.name, el.data.cardholder, el.data.cvv2, el.data.number, el.data.pin);
		} else if (el.type == 'note') {
			map.note += createNote(el.name, el.data.text);
		}
	}

	map.site = accordion(map.site);
	map.app = accordion(map.app);
	map.bookmark = accordion(map.bookmark);
	map.card = accordion(map.card);
	map.note = accordion(map.note);

	return map;
}
