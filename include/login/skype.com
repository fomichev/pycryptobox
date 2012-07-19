{
	"type":"login",
	"name": "Skype",
	"address": "https://login.skype.com/account/login-form?setlang=ru&return_url=https%3A%2F%2Fsecure.skype.com%2Faccount%2Flogin",
	"form":
	{
		"action": "https://login.skype.com/intl/ru/account/login-form",
		"method": "post",
		"fields":
		{
			"pie": "@token",
			"etm": "@token",
			"js_time": "",
			"timezone_field": "@token",
			"username": "@name@",
			"password": "@password@",
			"blackbox": "@token",
			"session_token": "@token"
		}
	}
}
