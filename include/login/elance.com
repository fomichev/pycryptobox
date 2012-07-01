{
	"type":"login",
	"name": "Elance",
	"address": "https://www.elance.com/php/landing/main/login.php",
	"form":
	{
		"action": "https://www.elance.com/php/reg/main/signInAHR.php",
		"method": "post",
		"fields":
		{
			"mode": "signin",
			"crypted": "",
			"redirect": "",
			"login_type": "",
			"token": "@token",
			"lnm": "$username",
			"pwd": "$password",
			"keepmesignin": "on"
		}
	}
}
