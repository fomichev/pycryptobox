{
	"type":"login",
	"name": "Spool",
	"address": "https://getspool.com/login",
	"form":
	{
		"action": "",
		"method": "post",
		"fields":
		{
			"login_email": "$username",
			"login_password": "$password",
			"login_button": "Login"
		}
	}
}
