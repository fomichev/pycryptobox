{
	"type":"login",
	"name": "OZON.ru",
	"address": "http://www.ozon.ru/?context=login",
	"form":
	{
		"action": "http://www.ozon.ru/default.aspx?context=login",
		"method": "post",
		"fields":
		{
			"LoginGroup": "HasAccountRadio",
			"Login": "$username",
			"Password": "$password",
			"CapabilityAgree": "on",
			"LoginGroup": "NewUserRadio"
		}
	}
}
