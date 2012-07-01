{
	"type":"login",
	"name": "Element14",
	"address": "http://www.element14.com/community/index.jspa#",
	"form":
	{
		"action": "https://www.element14.com/community/cs_login",
		"method": "post",
		"fields":
		{
			"username": "$username",
			"password": "$password",
			"autoLogin": "false"
		}
	}
}
