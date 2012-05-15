function loginWithToken(url, name, keys, values, token) {
	$("#div-token").dialog({
		height: 140,
		width: 280,
		modal: true,
		buttons: {
			"Login": function() {
				var token_value = $("#input-token").val();

				if (!token_value || token_value == "")
					return;

				keys.push(token);
				values.push(token_value);

				$("#input-token").val("");
				$(this).dialog('close');
				login("post", url, name, keys, values);
			},
			"Cancel": function() { $(this).dialog('close'); }
		}
	});
}

function login(method, url, name, keys, values) {
	var newWindow = window.open(url, name);
	if (!newWindow)
		return false;

	var html = "";
	html += "<html><head></head><body><form id='formid' method='" + method + "' action='";
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
