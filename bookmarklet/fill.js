function sitename(t) {
	return t.replace(/[^/]+\/\/([^/]+).+/, '$1').replace(/^www./, '');
}

function formToLink(name, vars, form) {
	var divStyle = 'style="border: 0 none; border-radius: 6px; background-color: #111; padding: 10px; margin: 5px; text-align: left;"';
	var aStyle = 'style="color: #fff; font-size: 18px; text-decoration: none;"';

	return '<div ' + divStyle + '><a ' + aStyle + ' href="#" onClick=\'javascript:' +
		'formFill(' + JSON.stringify(form) + ');' +
		'return false;\'>' + vars.username + '</a></div>';
}

function formFill(form) {
	var nodes = document.querySelectorAll("input[type=text], input[type=password]");
	for (var i = 0; i < nodes.length; i++) {
		var value = null;

		for (var field in form.fields)
			if (field == nodes[i].attributes['name'].value)
				value = form.fields[field];

		if (value)
			nodes[i].value = value;
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
				throw("<?text_incorrect_password?>");

			continue;
		}

		var address = sitename(document.URL);
		var action = sitename(el.form.action);

		if (address == action)
			matched.push(el);
	}

	if (matched.length == 0) {
		caption.innerHTML = '<?text_login_not_found?>';
		window.setTimeout(function () { document.body.click(); }, 1000)
	} else if (matched.length == 1) {
		caption.innerHTML = '<?text_wait_for_login?>';
		formFill(matched[0].form);
	} else {
		var r = ''
		for (var i = 0; i < matched.length; i++) {
			var el = matched[i];
			r += formToLink(el.name, el.vars, el.form);
		}

		caption.innerHTML = '<?text_select_login?>' + r;
	}
}

var div = document.createElement('div');
div.style.textAlign = 'center';

var caption = document.createElement('h1');
caption.appendChild(document.createTextNode('<?text_enter_password?>'));
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
buttonUnlock.value = "<?text_button_unlock?>";

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
		caption.innerHTML = e;

		window.setTimeout(function () { document.body.click(); }, 1000);
	}
	return false;
}

showPopover('320', '165', div);

input.focus();
