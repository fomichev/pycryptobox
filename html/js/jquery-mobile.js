function collapsible(name, value) {
	return '<div data-role="collapsible"><h3>' + name + '</h3><p>' + value + '</p></div>';
}

function page(id, header, data) {
	var t = '';

	t += '<div data-role="page" id="' + id + '" class="generated">';
	t += '<div data-role="header">';
	t += '<h1>' + header + '</h1>';
	t += '<a data-rel="back" href="#">Back</a>';
	t += '<a class="button-lock" href="#" data-icon="delete">Lock</a>';
	t += '</div>';
	t += '<div data-role="content">';
	t += data;
	t += '</div>';
	t += '</div>';

	return t;
}

function createLink(id, name, address, form, username, password) {
	var flat = flattenMap(form.fields);

	var title = name + " (" + username + ")";
	var t = '';

	if (withToken(form) == "") {
		t += '<a href="#todo" onClick=';
		
		t += '\'javascript:login("' + form.method + '", "' + form.action + '", "' + name + '", ' + flat.k + ', ' + flat.v + '); return false;\'';
		t += 'data-role="button">Login</a>';
	}

	t += '<a href="' + address + '" data-role="button">Go to site</a>';
	t += collapsible("Show username", username);
	t += collapsible("Show password", password);

	return page(id, title, t);
}

function createApp(id, name, key) {
	return page(id, name, key);
}

function createBookmark(id, name, url, comment) {
	return page(id, name, '<a class="button-goto" href="' + url + '" target="_blank">Go to site</a><p>' + comment + '</p>');
}

function createCard(id, name, cardholder, cvv2, number, pin) {
	var d = "";
	d += "<p>Cardholder=" + cardholder + "</p>";
	d += "<p>Number=" + number + "</p>";
	d += "<p>CVV2=" + cvv2 + "</p>";
	d += "<p>PIN=" + pin + "</p>";

	return page(id, name, d);
}

function createNote(id, name, text) {
	return page(id, name, text);
}

function viewCreatePageEntry(id, type, data) {
	if (type == 'site')
		return createLink(id, data.name, data.address, data.form, data.vars.username, data.vars.password);
	else if (type == 'app')
		return createApp(id, data.name, data.data.key);
	else if (type == 'bookmark')
		return createBookmark(id, data.name, data.data.url, data.data.comment);
	else if (type == 'card')
		return createCard(id, data.name, data.data.cardholder, data.data.cvv2, data.data.number, data.data.pin);
	else if (type == 'note')
		return createNote(id, data.name, data.data.text);
	else
		return '';
}

function viewCreateListEntry(id, type, data) {
	return '<li><a href="#' + id + '" class="generated">' + data.name + '</a></li>';
}

function viewWrapPageTag(tag, text) {
	return text;
}

function viewWrapListTag(tag, text) {
	if (tag != '__default__')
		tag = '<li data-role="list-divider">' + tag + '</li>';
	else
		tag = '';

	return tag + text;
}

function viewWrapList(text) {
	return '<ul data-role="listview" data-inset="true" data-filter="true">' + text + '</ul>';
}
