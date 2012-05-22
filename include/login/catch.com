{
	"type":"login",
	"name": "Catch.com",
	"address": "https://catch.com/",
	"form":
	{
		"action": "https://catch.com/login/catch",
		"method": "post",
		"fields":
		{
			"fromForm": "true",
			"email": "$username",
			"password": "$password",
			"keep": "on"
		}
	}
}
