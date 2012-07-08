{
	"type":"login",
	"name": "Audible.com",
	"address": "https://www.audible.com/sign-in",
	"form":
	{
		"action": "https://www.audible.com/sign-in/ref=ah_signin",
		"method": "post",
		"fields":
		{
			"email": "$name",
			"password": "$password",
			"appActionToken": "@token",
			"appAction": "audibleAction",
			"rdpath": "",
			"metadata1": "@token"
		}
	}
}
