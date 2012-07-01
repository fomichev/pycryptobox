{
	"type":"login",
	"name": "PodFM",
	"address": "http://podfm.ru/",
	"form":
	{
		"action": "http://podfm.ru/login/",
		"method": "post",
		"fields":
		{
			"a_todo": "login_check",
			"todo": "login",
			"login": "$username",
			"password": "$password",
			"remember": "off"
		}
	}
}
