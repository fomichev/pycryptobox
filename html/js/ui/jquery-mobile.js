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

function createLogin(id, name, address, form, username, password) {
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

function viewCreatePageEntry(id, type, data) {
	if (type == 'Logins')
		return createLogin(id, data.name, data.address, data.form, data.vars.username, data.vars.password);
	else {
		if (data.mtext != undefined)
			return page(id, data.name, addBr(data.mtext));
		else
			return page(id, data.name, addBr(data.text));
	}
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

function viewWrapPage(text) {
	return text;
}

function viewWrapList(text) {
	return '<ul data-role="listview" data-inset="true" data-filter="true">' + text + '</ul>';
}

function lock() {
	lockTimeoutStop();

	$(".generated").remove();
	$.mobile.changePage("#login", "slideup");
}
$(document).ready(function() {

	$("#form-unlock").submit(function(event) {
		event.preventDefault();

		try {
			var map = unlock($("#input-password").val());
			$("#input-password").val("");

			for (var key in map.list) {

				var pages_list = '';
				var pages = "";
				for (var key in map.page) {
					pages_list += '<li><a href="#' + key + '">' + key + '</a></li>'
					pages += page(key, key, map.list[key]);
					pages += map.page[key];
				}

				$("#ul-pages-list").html(pages_list);
				$("body").append(pages);
			}

			lockTimeoutStart();
		} catch(e) {
			alert("Incorrect password! " + e);
			return;
		}

		$.mobile.changePage("#main", "slideup");
	});

	$(".button-lock").click(function () {
		lock();
	});

	$("#input-password").focus();
});
