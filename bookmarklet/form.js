function openPre(data)
{
	var newWindow = window.open();
	if (!newWindow)
		return false;

	var html = "";
	html += "<html><head></head><body><pre>";
	html += data;
	html += "</pre>";

	newWindow.document.write(html);
	return newWindow;
}

var address = document.URL;
var name = document.title;
var body = document.getElementsByTagName("body")[0];
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

openPre(text);
