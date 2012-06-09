function sitename(t) {
	return t.replace(/[^/]+\/\/([^/]+).+/, '$1').replace(/^www./, '');
}

function formToLink(name, vars, form) {
	var r = "";
	var flat = flattenMap(form.fields);

	bg.style.border = '0 none';
	bg.style.borderRadius = '6px';

	var divStyle = 'style="border: 0 none; border-radius: 6px; background-color: #111; padding: 10px; margin: 5px; text-align: left;"';
	var aStyle = 'style="color: #fff; font-size: 18px; text-decoration: none;"';

	var token = withToken(form);
	if (token != "") {
		r += '<div ' + divStyle + '><a class="button-login" ' + aStyle + ' href="#" onClick=\'javascript:loginWithTokenData(false, "' + form.action + '", "' + name + '", ' + flat.k + ', ' + flat.v + ', ' + getFormsJson() + '); return false;\'>' + vars.username + '</a></div>';
	} else {
		r += '<div ' + divStyle + '><a class="button-login" ' + aStyle + ' href="#" onClick=\'javascript:login(false, "' + form.method + '", "' + form.action + '", "' + name + '", ' + flat.k + ', ' + flat.v + '); return false;\'>' + vars.username + '</a></div>';
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

function close(bg) {
	bg.style.display = 'none';
	bg.parentNode.removeChild(bg);
}

function showUnlock() {
	iframe = document.createElement('iframe');
	iframe.style.background = '#000';
	iframe.style.opacity = 0.8;
	iframe.style.position = 'absolute';
	iframe.style.zIndex = 99999;
	iframe.style.top = '20px';
	iframe.style.left = '20px';
	iframe.style.width = '320px';
	iframe.style.height = '165px';
	iframe.style.border = '0 none';
	iframe.style.borderRadius = '6px';
	iframe.style.boxShadow = '0 0 8px rgba(0,0,0,.8)';
	document.body.appendChild(iframe);

	bg = iframe.contentWindow.document.body;
	bg.style.color = '#fff';
	bg.style.textAlign = 'center';
	bg.paddingTop = '20px';

	var caption = document.createElement('h1');
	caption.appendChild(document.createTextNode('Enter password'));
	bg.appendChild(caption);

	form = document.createElement('form');

	input = document.createElement('input');
	input.type = "password";
	input.style.border = "1px solid #006";
	input.style.fontSize = '18px';

	buttonUnlock = document.createElement('input');
	buttonUnlock.type = "submit";
	buttonUnlock.style.border = "1px solid #006";
	buttonUnlock.style.fontSize = '14px';
	buttonUnlock.value = "Unlock";

	buttonDiv = document.createElement('div');
	buttonDiv.style.marginTop = '20px';
	buttonDiv.appendChild(buttonUnlock);

	form.appendChild(input);
	form.appendChild(buttonDiv);
	bg.appendChild(form);

	document.body.onclick = function() {
		close(bg);
	}

	bg.onclick = function(e) { e.stopPropagation(); }

	form.onsubmit = function() {
		try {
			bg.removeChild(form);
			bg.removeChild(caption);

			unlock(input.value, bg);
		} catch(e) {
			var c = document.createElement('h1');
			c.appendChild(document.createTextNode('Invalid password'));
//			c.appendChild(document.createTextNode(e));
			bg.appendChild(c);

			window.setTimeout(function () { close(bg); }, 1000)
		}
		return false;
	}

	input.focus();
}

function unlock(pwd, bg) {
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
		bg.innerHTML = '<h1>No logins found!</h1>';
		window.setTimeout(function () { close(bg); }, 1000)
	} else if (matched.length == 1) {
		bg.innerHTML = '<h1>Logging in...</h1>';
		formLogin(matched[0].form);
	} else {
		var r = ''
		for (var i = 0; i < matched.length; i++) {
			var el = matched[i];
			r += formToLink(el.name, el.vars, el.form);
		}

		bg.innerHTML = '<h1>Select login</h1>' + r;
	}
}

//window.onload = function() {
showUnlock();
//}
