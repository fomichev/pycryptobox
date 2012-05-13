function createCard(name, cardholder, cvv2, number, pin) {
	var d = "";
	d += "<p>Cardholder=" + cardholder + "</p>";
	d += "<p>Number=" + number + "</p>";
	d += "<p>CVV2=" + cvv2 + "</p>";
	d += "<p>PIN=" + pin + "</p>";

	var r = "";

	r += "<h1>" + name + "</h1>";
	r += '<p>' + createHiddenOnClick("Detailed data", d) + '</p>';

	return r;
}

function createNote(name, text) {
	var r = "";

	r += "<h1>" + name + "</h1>";
	r += '<p>' + createHiddenOnClick("Detailed data", text) + '</p>';

	return r;
}

function withToken(form) {
	for (var key in form.fields) {
		var value = form.fields[key];

		if (value == "@token")
			return key;
	}

	return "";
}

function createLink(name, address, form, username, password) {
	var url = form.action;
	var title = name + " (" + username + ")"

	var k = "";
	var v = "";

	var r = "";

	for (var key in form.fields) {
		if (form.fields[key] == "@token")
			continue;

		if (k == "") {
			k = "new Array(\"" + key +"\"";
			v = "new Array(\"" + form.fields[key] +"\"";
		} else {
			k += ", \"" + key +"\"";
			v += ", \"" + form.fields[key] +"\"";
		}
	}
	k += ")"
	v += ")"

	r += "<h1>";

	var token = withToken(form);
	if (token != "") {
		r += "<a href='#' onClick='javascript:openPostWithToken(\"" + url + "\", \"" + name + "\", " + k + ", " + v + ", \"" + token + "\"); return false;'>" + title + "</a>"
		r += ' - <a href="' + address + '" target="_blank">Obtain token</a>';
	} else {
		if (form.method == "post")
			r += "<a href='#' onClick='javascript:openPost(\"" + url + "\", \"" + name + "\", " + k + ", " + v + "); return false;'>" + title + "</a>"
		else
			r += "GET METHOD FOR " + name + "IS NOT IMPLEMENTED"

	}
	r += "</h1>";


	r += '<p><a href="' + address + '" target="_blank">Go to site</a></p>';
	r += '<p>' + createHiddenOnClick("Username: ********", username) + '</p>';
	r += '<p>' + createHiddenOnClick("Password: ********", password) + '</p>';

	return r;
}

var hocid = 0;
function createHiddenOnClick(name, value) {
	var id = "hoc" + hocid;
	var id_h = id + "_h";

	hocid++;

	var ret = "";
	
	ret += '<div id="' + id + '">' + name + ' ';
	ret += '<a href="#" onClick="javascript:document.getElementById(\'' + id_h + '\').className=\'unhidden\';document.getElementById(\'' + id + '\').className=\'hidden\';return false;"> (Reveal)</a>';
	ret += '</div>';


	ret += '<div id="' + id_h + '" class="hidden">' + value + ' ';
	ret += '<a href="#" onClick="javascript:document.getElementById(\'' + id + '\').className=\'unhidden\';document.getElementById(\'' + id_h + '\').className=\'hidden\';return false;"> (Hide)</a>';
	ret += '</div>';

	return ret;
}
