function createCard(name, cardholder, cvv2, number, pin) {
	var d = "";
	d += "<p>Cardholder=" + cardholder + "</p>";
	d += "<p>Number=" + number + "</p>";
	d += "<p>CVV2=" + cvv2 + "</p>";
	d += "<p>PIN=" + pin + "</p>";

	var r = "";

	r += "<h1>" + name + "</h1>";
	r += '<p>' + createHiddenOnClick("Show detailed data", d) + '</p>';

	return r;
}

function createNote(name, text) {
	var r = "";

	r += "<h1>" + name + "</h1>";
	r += '<p>' + createHiddenOnClick("Show note", text) + '</p>';

	return r;
}

function createLink(name, address, form, username, password) {
	var url = form.action;

	var k = "";
	var v = "";

	var r = "";

	for (var key in form.fields) {
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
	if (form.method == "post")
		r += "<a href='#' onClick='javascript:openPost(\"" + url + "\", \"" + name + "\", " + k + ", " + v + ");'>" + name + "</a>"
	else
		r += "GET METHOD FOR " + name + "IS NOT IMPLEMENTED"
	r += "</h1>";


	r += '<p>' + createHiddenOnClick("Show username", username) + '</p>';
	r += '<p>' + createHiddenOnClick("Show password", password) + '</p>';

	return r;
}

var hocid = 0;
function createHiddenOnClick(visible, invisible) {
	var id = "hoc" + hocid;
	var id_h = id + "_h";

	hocid++;

	var ret = "";
	
	ret += "<div id=\"" + id + "\" onClick='javascript:document.getElementById(\"" + id_h + "\").className=\"unhidden\";this.className=\"hidden\"'>" + visible + "</div>";
	ret += "<div class=\"hidden\" id=\"" + id_h + "\" onClick='javascript:document.getElementById(\"" + id + "\").className=\"unhidden\";this.className=\"hidden\"'>" + invisible + "</div>";

	return ret;
}
