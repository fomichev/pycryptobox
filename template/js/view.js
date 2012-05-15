function copyToClipboard(text) {
	var t = '';
	var pathToClippy = 'clippy.swf';

        t += '<object classid="clsid:d27cdb6e-ae6d-11cf-96b8-444553540000" width="110" height="14">';
        t += '<param name="movie" value="' + pathToClippy + '"/>';
        t += '<param name="allowScriptAccess" value="always" />';
        t += '<param name="quality" value="high" />';
        t += '<param name="scale" value="noscale" />';
        t += '<param NAME="FlashVars" value="text=#' + text + '">';
        t += '<param name="bgcolor" value="#fff">';
        t += '<embed src="' + pathToClippy + '" width="110" height="14" name="clippy" quality="high" allowScriptAccess="always" type="application/x-shockwave-flash" pluginspage="http://www.macromedia.com/go/getflashplayer" FlashVars="text=' + text + '" bgcolor="#fff" />';
        t += '</object>';

	return t;
}

function withToken(form) {
	for (var key in form.fields) {
		var value = form.fields[key];

		if (value == "@token")
			return key;
	}

	return "";
}

function flattenMap(map) {
	var k = "";
	var v = "";

	for (var key in map) {
		if (map[key] == "@token")
			continue;

		if (k == "") {
			k = "new Array(\"" + key +"\"";
			v = "new Array(\"" + map[key] +"\"";
		} else {
			k += ", \"" + key +"\"";
			v += ", \"" + map[key] +"\"";
		}
	}
	k += ")"
	v += ")"

	var r = {};
	r.k = k;
	r.v = v;

	return r;
}

function unlock(pwd) {
	var text = decrypt(pwd, _cfg_salt, _cfg_cipher);
	var data = eval(text);
	var map = {};

	if (data[0].type != "magic" || data[0].value != "270389")
		throw "Wrong magic number";

	map.listSite = "";
	map.listApp = "";

	map.site = "";
	map.app = "";
	map.bookmark = "";
	map.card = "";
	map.note = "";

	for (var i = 0; i < data.length; i++) {
		var el = data[i];

		if (el.type == 'site') {
			map.listSite += createList("site_" + i, el.name + ' (' + el.vars.username + ')');
			map.site += createLink("site_" + i, el.name, el.address, el.form, el.vars.username, el.vars.password);
		} else if (el.type == 'app') {
			map.listApp += createList("app_" + i, el.name);
			map.app += createApp("app_" + i, el.name, el.data.key);
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
