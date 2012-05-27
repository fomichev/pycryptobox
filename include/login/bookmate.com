{
	"type":"login",
	"name": "Bookmate",
	"address": "http://bookmate.com/login?return_to=%2F",
	"broken": "1",
	"form":
	{
		"action": "http://bookmate.com/login",
		"method": "post",
		"fields":
		{
			"utf8": "✓",
			"authenticity_token": "@token",
			"user_session[login]": "$username",
			"user_session[password]": "$passworf",
			"not_remember_me": "1"
		}
	}
}
