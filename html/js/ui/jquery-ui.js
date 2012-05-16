function accordionItem(header, body) {
	return '<h3><a href="#">' + header + '</a></h3><div>' + body + '</div>';
}

function createLogin(id, name, address, form, username, password) {
	var hocid = 0;
	function collapsible(name, value) {
		return '<div class="expand"><a href="#" onClick="javascript:return false;"><strong>' + name + '</strong> (click to expand/collapse)</a></div><div>' + value + '</div>';
	}

	var title = name + " (" + username + ")"

	var r = "";
	var flat = flattenMap(form.fields);

	var token = withToken(form);
	if (token != "") {
		r += '<a class="button-bookmark" href="' + address + '" target="_blank">Get token</a>';
		r += '<a class="button-login" href="#" onClick=\'javascript:loginWithToken("' + form.action + '", "' + name + '", ' + flat.k + ', ' + flat.v + ', new Array(' + token + ')); return false;\'>Log in</a>';
	} else {
		r += '<a class="button-login" href="#" onClick=\'javascript:login("' + form.method + '", "' + form.action + '", "' + name + '", ' + flat.k + ', ' + flat.v + '); return false;\'>Log in</a>';
	}

	r += '<a class="button-goto" href="' + address + '" target="_blank">Go to site</a>';
	r += '<p>' + collapsible("Username", username + ' ' + copyToClipboard(username)) + '</p>';
	r += '<p>' + collapsible("Password", password + ' ' + copyToClipboard(password)) + '</p>';

	return accordionItem(title, r);
}

function viewCreatePageEntry(id, type, data) {
	if (type == 'Logins')
		return createLogin(id, data.name, data.address, data.form, data.vars.username, data.vars.password);
	else
		return accordionItem(data.name, addBr(data.text));
}

function viewCreateListEntry(id, type, data) {
	return "";
}

function viewWrapPageTag(tag, text) {
	if (tag != '__default__')
		tag = '<h4>' + tag + '</h4>';
	else
		tag = '';

	return tag + '<div class="generated"><div class="accordion">' + text + '</div></div>';
}

function viewWrapListTag(tag, text) {
	return text;
}

function viewWrapPage(text) {
	return text;
}

function viewWrapList(text) {
	return text;
}

function lock() {
	lockTimeoutStop();

	if ($("#div-locked").is(":visible") && $("#div-unlocked").is(":visible")) {
		$("#div-generate").hide();
		$("#div-token").hide();
		$("#div-unlocked").hide();
	} else {
		$("#div-generate").dialog('close');
		$("#div-token").dialog('close');

		$("#div-locked").fadeIn();
		$("#div-unlocked").hide();
	}

	$(".generated").remove();
	$("#tabs").html('');
	$("#tabs").removeClass();

	$("#input-password").focus();
}

$(document).ready(function() {
	lock();

	$(".button").button();

	$("#button-unlock").button({ icons: { primary: "ui-icon-unlocked" } });
	$("#button-lock").button({ icons: { primary: "ui-icon-locked" } });
	$("#button-generate-show").button({ icons: { primary: "ui-icon-gear" } });

	$("#form-unlock").submit(function(event) {
		event.preventDefault();
		try {
			var map = unlock($("#input-password").val());
			$("#input-password").val("");

			var tabs_list = '';
			var tabs = "";
			for (var key in map.page) {
				tabs_list += '<li><a href="#div-' + key + '">' + key + '</a></li>';
				tabs += '<div id="div-' + key +'" class="generated">' + map.page[key] + '</div>';
			}

			$("#div-tabs").html('<div id="tabs"><ul class="generated">' + tabs_list + '</ul>' + tabs + '</div>');

			$(".button").button();
			$(".accordion").accordion({
				autoHeight: false,
				navigation: false,
				active: false,
				collapsible: true
			});
			$('.expand').click(function() {
				event.preventDefault();
				$(this).next().toggle();
			}).next().hide();

			$("#tabs").tabs();

			$(".button-bookmark").button({ icons: { primary: "ui-icon-contact" } });
			$(".button-goto").button({ icons: { primary: "ui-icon-newwin" } });
			$(".button-login").button({ icons: { primary: "ui-icon-key" } });

			lockTimeoutStart();

			$("#div-locked").hide();
			$("#div-unlocked").fadeIn();
		} catch(e) {
			alert("Incorrect password! " + e);
			return;
		}
	});

	$("body").mousemove(function() { lockTimeoutUpdate(); });

	$("#button-lock").click(function(event) {
		event.preventDefault();
		lock();
	});

	$("#button-generate-show").click(function(event) {
		event.preventDefault();
		$("#div-generate").dialog({
			resizable: false,
			buttons: {
				"Generate": function() {
					$("#intput-generated-password").val(generatePassword(
						$("#input-password-length").val(),
						$("#input-include-num").is(":checked"),
						$("#input-include-punc").is(":checked"),
						$("#input-include-uc").is(":checked"),
						$("#input-pronounceable").is(":checked")));
				},
				"Cancel": function() { $(this).dialog('close'); }
			}
		});
	});

	$("#input-pronounceable").click(function() {
		if ($("#input-pronounceable").is(":checked")) {
			$("#input-include-num").attr("disabled", true);
			$("#input-include-punc").attr("disabled", true);
		} else {
			$("#input-include-num").removeAttr("disabled");
			$("#input-include-punc").removeAttr("disabled");
		}
	});
});
