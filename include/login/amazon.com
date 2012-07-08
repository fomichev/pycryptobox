{
	"type":"login",
	"name": "Amazon.com",
	"address": "https://www.amazon.com/ap/signin?_encoding=UTF8&openid.assoc_handle=usflex&openid.return_to=https%3A%2F%2Fwww.amazon.com%2Fgp%2Fyourstore%2Fhome%3Fie%3DUTF8%26ref_%3Dgno_signin&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.pape.max_auth_age=0&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select",
	"form":
	{
		"broken": true,
		"action": "https://www.amazon.com/ap/signin",
		"method": "post",
		"fields":
		{
			"appActionToken": "@token",
			"appAction": "SIGNIN",
			"openid.pape.max_auth_age": "@token",
			"openid.ns": "@token",
			"openid.ns.pape": "@token",
			"pageId": "@token",
			"openid.identity": "@token",
			"openid.claimed_id": "@token",
			"openid.mode": "@token",
			"openid.assoc_handle": "@token",
			"openid.return_to": "@token",
			"email": "",
			"create": "1",
			"create": "0",
			"password": "",
			"metadata1": "@token"
		}
	}
}
