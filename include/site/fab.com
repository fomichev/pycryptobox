{
	"type":"site",
	"name": "Fab.com",
	"address": "http://fab.com/",
	"form":
	{
		"action": "https://fab.com/?",
		"method": "post",
		"fields":
		{
			"utf8": "✓",
			"user[un_or_email]": "$username",
			"user[password]": "$password",
			"user[form_type]": "login",
			"user[referrer_url]": "",
			"invitecode": "",
			"fref": "",
			"frefl": "",
			"nan_pid": ""
		}
	}
}
