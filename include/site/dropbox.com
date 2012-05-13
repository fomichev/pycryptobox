{
	"type": "site",
	"name": "Dropbox ($username)",
	"address": "https://www.dropbox.com/",
	"form":
	{
		"action":"https://www.dropbox.com/login",
		"method": "post",
		"fields":
		{
			"login_email": "$username",
			"login_password": "$password",
			"remember_me": "on",
			"cont": "/home"
		}
	}
}
