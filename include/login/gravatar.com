{
	"type":"login",
	"name": "Gravatar",
	"address": "https://en.gravatar.com/site/login/",
	"form":
	{
		"action": "https://en.gravatar.com/sessions/",
		"method": "post",
		"fields":
		{
			"user": "$username",
			"pass": "$password",
			"commit": "Login"
		}
	}
}
