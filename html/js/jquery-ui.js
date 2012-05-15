function accordionItem(header, body) {
	return '<h3><a href="#">' + header + '</a></h3><div>' + body + '</div>';
}

function createList(id, name) {
	return "";
}

function createLink(id, name, address, form, username, password) {
	var hocid = 0;
	function collapsible(name, value) {
		return '<div class="expand"><a href="#" onClick="javascript:return false;"><strong>' + name + '</strong> (click to expand/collapse)</a></div><div>' + value + '</div>';
	}

	var title = name + " (" + username + ")"

	var r = "";
	var flat = flattenMap(form.fields);

	var token = withToken(form);
	if (token != "") {
		r += '<a class="button-token" href="' + address + '" target="_blank">Get token</a>';
		r += '<a class="button-login" href="#" onClick=\'javascript:loginWithToken("' + form.action + '", "' + name + '", ' + flat.k + ', ' + flat.v + ', "' + token + '"); return false;\'>Login</a>';
	} else {
		r += '<a class="button-login" href="#" onClick=\'javascript:login("' + form.method + '", "' + form.action + '", "' + name + '", ' + flat.k + ', ' + flat.v + '); return false;\'>Login</a>';
	}

	r += '<a class="button-goto" href="' + address + '" target="_blank">Go to site</a>';
	r += '<p>' + collapsible("Username", username + ' ' + copyToClipboard(username)) + '</p>';
	r += '<p>' + collapsible("Password", password + ' ' + copyToClipboard(password)) + '</p>';

	return accordionItem(title, r);
}

function createApp(id, name, key) {
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
	return '<div class="generated"><div class="accordion">' + text + '</div></div>';
}
