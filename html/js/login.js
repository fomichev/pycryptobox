function withToken(form) {
	var tokens = "";

	if (form.action == '@token')
		return "__form_action__";

	for (var key in form.fields) {
		var value = form.fields[key];

		if (value == "@token") {
			if (tokens == "")
				tokens = '"' + key + '"';
			else
				tokens += ', "' + key + '"';
		}
	}

	return tokens;
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
	if (k != "")
		k += ")";

	if (v != "")
		v += ")";

	var r = {};
	r.k = k;
	r.v = v;

	return r;
}

function loginWithTokenData(url, name, keys, values, formJson)
{
	try {
		var data = eval(formJson);
		for (var i = 0; i < data.length; i++) {
			for (var field in data[i].form.fields) {
				if (tokens.indexOf(field) >= 0) {
					keys.push(field);
					values.push(data[i].form.fields[field]);
				}
			}
		}
	} catch(e) {
		return;
	}

	login("post", url, name, keys, values);
}

function login(withNewWindow, method, url, name, keys, values) {
	var newWindow = null;
	if (withNewWindow) {
		var newWindow = window.open(url, name);
		if (!newWindow)
			return false;
	} else {
		newWindow = window;
		document.close();
		document.open();
	}

	var html = "";
	html += "<html><head></head><body><?text_wait_for_login?><form id='formid' method='" + method + "' action='";
	html +=url;
	html += "'>";

	if (keys && values && (keys.length == values.length))
		for (var i=0; i < keys.length; i++)
			html += "<input type='hidden' name='" + keys[i] + "' value='" + values[i] + "'/>";
			html += "</form><script type='text/javascript'>document.getElementById('formid').submit()</s";
			/* &lt;/script&gt; screws everything up after embedding,
			 * so split it into multiple lines */
			html += "cript></body></html>";

	newWindow.document.write(html);
	return newWindow;
}

/* TODO: copied from bookmarklet/form.js; need to remove duplicity */
function getFormsJson() {
	var address = document.URL;
	var name = document.title;
	var text = "";

	for (var i = 0; i < document.forms.length; i++) {
		var form = document.forms[i];

		var form_elements =  "";
		for (var j = 0; j < form.elements.length; j++) {
			var el = form.elements[j];

			if (el.name == "")
				continue;

			if (form_elements == "")
				form_elements = '\t\t\t"' + el.name + '": "' + el.value + '"';
			else
				form_elements += ',\n\t\t\t"' + el.name + '": "' + el.value + '"';
		}

		var form_text = '\t\t"action": "' + form.action + '",\n\t\t"method": "' + form.method + '",\n\t\t"fields":\n\t\t{\n' + form_elements + '\n\t\t}';

		if (text == "")
			text += '[\n';
		else
			text += ',\n';
		text += '{\n\t"type":"login",\n\t"name": "' + name + '",\n\t"address": "' + address + '",\n\t"form":\n\t{\n' + form_text + '\n\t}\n}\n';
	}

	text += "]";

	return text;
}
