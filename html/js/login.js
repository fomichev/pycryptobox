function loginWithToken(url, name, keys, values, token) {
	$("#div-token").dialog({
		height: 140,
		width: 280,
		modal: true,
		buttons: {
			"Login": function() {
				var form_json = $("#input-json").val();
				var token_value = "";

				if (!form_json || form_json == "")
					return;

				var data = eval(form_json);
				for (var i = 0; i < data.length; i++) {
					for (var field in data[i].form.fields) {
						if (field == token) {
							token_value = data[i].form.fields[field];
							break;
						}
					}
				}

				if (token_value == "") {
					alert("Token value not found! Make sure form layout didn't change!");
					return;
				}

				keys.push(token);
				values.push(token_value);

				$("#input-json").val("");
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
