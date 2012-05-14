function accordionItem(header, body) {
	return '<h3><a href="#">' + header + '</a></h3><div>' + body + '</div>';
}

function createLink(name, address, form, username, password) {
	var hocid = 0;
	function createHiddenOnClick(name, value) {
		var id = "hoc" + hocid;
		var id_h = id + "_h";

		hocid++;

		var ret = "";

		/*
		ret += '<div id="' + id '">';
		ret += '<h3><a href="#">' + name + '</a></h3>';
		ret += '<div>' + value + '</div>';
		*/

		ret += '<div id="' + id + '">' + name + ' ';
		ret += '<a class="buttonSmall" href="#" onClick="javascript:document.getElementById(\'' + id_h + '\').className=\'unhidden\';document.getElementById(\'' + id + '\').className=\'hidden\';return false;">Reveal</a>';
		ret += '</div>';


		ret += '<div id="' + id_h + '" class="hidden">' + value + ' ';
		ret += '<a class="buttonSmall" href="#" onClick="javascript:document.getElementById(\'' + id + '\').className=\'unhidden\';document.getElementById(\'' + id_h + '\').className=\'hidden\';return false;">Hide</a>';
		ret += '</div>';

		return ret;
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
		r += '<a class="buttonSmall" href="' + address + '" target="_blank">Obtain token</a>';
		r += "<a class=\"buttonSmall\" href='#' onClick='javascript:openPostWithToken(\"" + url + "\", \"" + name + "\", " + k + ", " + v + ", \"" + token + "\"); return false;'>Login</a>"
	} else {
		if (form.method == "post")
			r += "<a class=\"buttonSmall\" href='#' onClick='javascript:openPost(\"" + url + "\", \"" + name + "\", " + k + ", " + v + "); return false;'>Login</a>"
		else
			r += "GET METHOD FOR " + name + "IS NOT IMPLEMENTED"

	}


	r += '<a class="buttonSmall" href="' + address + '" target="_blank">Go to site</a>';
	r += '<p>' + createHiddenOnClick("Username", username) + '</p>';
	r += '<p>' + createHiddenOnClick("Password", password) + '</p>';

	return accordionItem(title, r);
}

function createApp(name, key) {
	return accordionItem(name, key);
}

function createBookmark(name, url, comment) {
	return accordionItem(name, '<a href="' + url + '" target="_blank">Go!</a><p>' + comment + '</p>');
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

function unlock(pwd) {
	var text = decrypt(pwd, _cfg_salt, _cfg_cipher);
	var data = eval(text);
	var map = {};

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

	map.json = accordionItem("JSON", '<pre>' + text + '</pre>');

	return map;
}
