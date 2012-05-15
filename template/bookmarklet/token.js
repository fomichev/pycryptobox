function show(data)
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

	for (var j = 0; j < form.elements.length; j++) {
		var el = form.elements[j];

		if (el.name == "")
			continue;

		if (el.name.match("token") || el.name.match("__VIEWSTATE")) {
			text += el.name + ": " + el.value;
		}
	}
}

if (text == "")
	text = "No auth token found!";

show(text);
