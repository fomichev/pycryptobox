{
	"type":"login",
	"name": "LinkedIn",
	"address": "https://www.linkedin.com/uas/login",
	"form":
	{
		"action": "https://www.linkedin.com/uas/login-submit",
		"method": "post",
		"fields":
		{
			"source_app": "",
			"session_key": "$username",
			"session_password": "$password",
			"signin": "Sign In",
			"session_redirect": "",
			"csrfToken": "@token",
			"sourceAlias": "@token"
		}
	}
}