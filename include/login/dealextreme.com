{
	"type":"login",
	"name": "DealExtreme",
	"address": "http://www.dealextreme.com/accounts/default.dx",
	"form":
	{
		"action": "http://www.dealextreme.com/accounts/default.dx",
		"method": "post",
		"fields":
		{
			"__EVENTTARGET": "",
			"__EVENTARGUMENT": "",
			"__VIEWSTATE": "@token",
			"__EVENTVALIDATION": "@token",
			"ctl00$content$OrderNumber": "",
			"ctl00$content$EMail": "",
			"ctl00$content$Actions": "rbTrackStatus",
			"ctl00$content$Actions": "rbInvoice",
			"ctl00$content$Actions": "rbUpdateOrder",
			"ctl00$content$Actions": "rbRMA",
			"ctl00$content$Track": "Track Order",
			"ctl00$content$txtLoginEmail": "$username",
			"ctl00$content$txtPassword": "$password",
			"ctl00$content$btnAccountLogin": "Click here to Login"
		}
	}
}