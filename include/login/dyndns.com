{
	"type":"login",
	"name": "DynDNS",
	"address": "https://account.dyn.com/entrance/",
	"form":
	{
		"action": "https://account.dyn.com/entrance/",
		"method": "post",
		"fields":
		{
			"username": "$username",
			"password": "$password",
			"submit": "Log in",
			"multiform": "@token"
		}
	}
}