function openPostWithToken(url, name, keys, values, token) {
	var token_value = prompt("Enter token", "");
	if (token_value == "")
		return;

	keys.push(token);
	values.push(token_value);

	alert(keys);
	alert(values);

	openPost(url, name, keys, values);
}

function openPost(url, name, keys, values) {
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
			html += "</form><script type='text/javascript'>document.getElementById('formid').submit()</s";
			/* &lt;/script&gt; screws everything up after embedding,
			 * so split it into multiple lines */
			html += "cript></body></html>";

/*	alert(html); */

	newWindow.document.write(html);
	return newWindow;
}
