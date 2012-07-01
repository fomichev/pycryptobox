{
	"type":"login",
	"name": "IFTTT",
	"address": "https://ifttt.com/login",
	"form":
	{
		"action": "https://ifttt.com/session",
		"method": "post",
		"fields":
		{
			"utf8": "✓",
			"authenticity_token": "@token",
			"login": "$username",
			"password": "$password",
			"remember_me": "1",
			"commit": "Sign in"
		}
	}
}
