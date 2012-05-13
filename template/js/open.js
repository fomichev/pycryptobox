function openPost(url, name, keys, values)
{
	var newWindow = window.open(url, name);
	if (!newWindow)
		return false;

	var html = "";
	html += "<html><head></head><body><form id='formid' method='post' action='";
	html +=url;
	html += "'>";

	if (keys && values && (keys.length == values.length))
		for (var i=0; i < keys.length; i++)
			html += "<input type='hidden' name='" + keys[i] + "' value='" + values[i] + "'/>";
			html += "</form><script type='text/javascript'>document.getElementById('formid').submit()</script></body></html>";

/*	alert(html); */

	newWindow.document.write(html);
	return newWindow;
}
