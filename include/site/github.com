{
	"type":"site",
	"name": "GitHub",
	"address": "https://github.com/login",
	"form":
	{
		"action": "https://github.com/session",
		"method": "post",
		"fields":
		{
			"authenticity_token": "@AUTH_TOKEN",
			"login": "$username",
			"password": "$password",
			"commit": "Log in"
		}
	}
}
