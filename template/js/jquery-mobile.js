function collapsible(name, value) {
	return '<div data-role="collapsible"><h3>' + name + '</h3><p>' + value + '</p></div>';
}

function page(id, header, data) {
	var t = '';

	t += '<div data-role="page" id="' + id + '" class="generated">';
	t += '<div data-role="header">';
	t += '<h1>' + header + '</h1>';
	t += '<a data-rel="back" href="#">Back</a>';
	t += '</div>';
	t += '<div data-role="content">';
	t += data;
	t += '</div>';
	t += '</div>';

	return t;
}

function createList(id, name) {
	return '<li><a href="#' + id + '" class="generated">' + name + '</a></li>';
}

function createLink(id, name, address, form, username, password) {
	var flat = flattenMap(form.fields);

	var title = name + " (" + username + ")";
	var t = '';

	if (withToken(form) == "") {
		t += '<a href="#todo" onClick=';
		
		t += '\'javascript:login("' + form.method + '", "' + form.action + '", "' + name + '", ' + flat.k + ', ' + flat.v + '); return false;\'';
		t += 'data-role="button">Login</a>';
	} else {
		t += '<p>No one click login for forms with tokens!</p>';
	}

	t += collapsible("Show username", username);
	t += collapsible("Show password", password);

	return page(id, title, t);
}

function createApp(id, name, key) {
	return page(id, name, key);
}

function createBookmark(name, url, comment) {
	return "";
}

function createCard(name, cardholder, cvv2, number, pin) {
	return "";
}

function createNote(name, text) {
	return "";
}

function accordion(text) {
	return text;
}
