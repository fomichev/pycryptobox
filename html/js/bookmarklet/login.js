function sitename(t) {
	return t.replace(/[^/]+\/\/([^/]+).+/, '$1').replace(/^www./, '');
}

function formToLink(name, vars, form) {
	var r = "";
	var flat = flattenMap(form.fields);

	var divStyle = 'style="border: 0 none; border-radius: 6px; background-color: #111; padding: 10px; margin: 5px; text-align: left;"';
	var aStyle = 'style="color: #fff; font-size: 18px; text-decoration: none;"';

	var token = withToken(form);
	if (token != "") {
		r += '<div ' + divStyle + '><a ' + aStyle + ' href="#" onClick=\'javascript:loginWithTokenData(false, "' + form.action + '", "' + name + '", ' + flat.k + ', ' + flat.v + ', ' + getFormsJson() + '); return false;\'>' + vars.username + '</a></div>';
	} else {
		r += '<div ' + divStyle + '><a ' + aStyle + ' href="#" onClick=\'javascript:login(false, "' + form.method + '", "' + form.action + '", "' + name + '", ' + flat.k + ', ' + flat.v + '); return false;\'>' + vars.username + '</a></div>';
	}

	return r;
}

function formLogin(form) {
	var flat = flattenMap(form.fields);
	var keys = eval(flat.k);
	var values = eval(flat.v);

	var token = withToken(form);
	if (token != "") {
		token = eval('new Array(' + token + ')');
		loginWithTokenData(false, form.action, name, keys, values, getFormsJson());
	} else {
		login(false, form.method, form.action,  name, keys, values);
	}
}

function unlock(pwd, caption) {
	var text = decrypt(pwd, cfg.pbkdf2.salt, cfg.cipher, cfg.pbkdf2.iterations, cfg.aes.iv);
	var data = eval(text);
	var matched = new Array();

	for (var i = 0; i < data.length; i++) {
		var el = data[i];
		if (el.type == "magic") {
			if (el.value != "270389")
				throw("Invalid password!");

			continue;
		}

//		var address = sitename("http://dropbox.com/asdfadfqw");
		var address = sitename(document.URL);
		var action = sitename(el.form.action);

		if (address == action)
			matched.push(el);
	}


	if (matched.length == 0) {
		caption.innerHTML = 'No logins found!';
		window.setTimeout(function () { document.body.click(); }, 1000)
	} else if (matched.length == 1) {
		caption.innerHTML = 'Logging in...';
		formLogin(matched[0].form);
	} else {
		var r = ''
		for (var i = 0; i < matched.length; i++) {
			var el = matched[i];
			r += formToLink(el.name, el.vars, el.form);
		}

		caption.innerHTML = 'Select login' + r;
	}
}

var div = document.createElement('div');
div.style.textAlign = 'center';

var caption = document.createElement('h1');
caption.appendChild(document.createTextNode('Enter password'));
div.appendChild(caption);

var form = document.createElement('form');

var input = document.createElement('input');
input.type = "password";
input.style.border = "1px solid #006";
input.style.fontSize = '18px';

var buttonUnlock = document.createElement('input');
buttonUnlock.type = "submit";
buttonUnlock.style.border = "1px solid #006";
buttonUnlock.style.fontSize = '14px';
buttonUnlock.value = "Unlock";

var buttonDiv = document.createElement('div');
buttonDiv.style.marginTop = '20px';
buttonDiv.appendChild(buttonUnlock);

form.appendChild(input);
form.appendChild(buttonDiv);
div.appendChild(form);

form.onsubmit = function() {
	try {
		div.removeChild(form);

		unlock(input.value, caption);
	} catch(e) {
//		caption.innerHTML = 'Invalid password';
		caption.innerHTML = e;

		window.setTimeout(function () { document.body.click(); }, 1000);
	}
	return false;
}

showPopover('320', '165', div);

input.focus();
