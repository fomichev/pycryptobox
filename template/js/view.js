function createLink(name, address, form) {
	var url = form.action;

	var k = "";
	var v = "";

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

	if (form.method == "post")
		return "<a href='#' onClick='javascript:openPost(\"" + url + "\", \"" + name + "\", " + k + ", " + v + ");'>" + name + "</a>"
	else
		return "GET METHOD FOR " + name + "IS NOT IMPLEMENTED"
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
