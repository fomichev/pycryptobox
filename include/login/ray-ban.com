{
	"type":"login",
	"name": "Ray Ban",
	"address": "https://www.ray-ban.com/usa/customer/account/login/",
	"form":
	{
		"action": "https://www.ray-ban.com/usa/customer/account/loginPost/",
		"method": "post",
		"fields":
		{
			"login[username]": "$username",
			"login[password]": "$password",
			"send": ""
		}
	}
}
