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
	var form_elements =  "len = " + document.forms[i].elements.length;
	for (var j = 0; j < document.forms[i].elements.length; j++) {
		var el = document.forms[i].elements[j];

		if (el.name != "") {
			if (form_elements == "")
				form_elements = '\t\t\t"' + el.name + '": "' + el.value + '"';
			else
				form_elements += ',\n\t\t\t"' + el.name + '": "' + el.value + '"';
		} else {
				form_elements += '((((' + el.id + '))))';
		}
	}

	var form_text = '\t\t"action": "' + document.forms[i].action + '",\n\t\t"method": "' + document.forms[i].method + '",\n\t\t"fields":\n\t\t{\n' + form_elements + '\n\t\t}';
	text += '{\n\t"type":"site",\n\t"name": "' + name + '",\n\t"address": "' + address + '",\n\t"form":\n\t{\n' + form_text + '\n\t}\n}\n';
}

openPre(text);
