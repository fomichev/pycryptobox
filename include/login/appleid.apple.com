{
	"type":"login",
	"name": "Apple ID",
	"address": "https://appleid.apple.com/cgi-bin/WebObjects/MyAppleId.woa/131/wa/directToSignIn?wosid=8BEW7xlvojhmv1LbtHulOw&localang=en_US",
	"form":
	{
		"action": "@token",
		"method": "post",
		"fields":
		{
			"0.29.145.1.1": "",
			"theAccountName": "$username",
			"theAccountPW": "$password",
			"signInHyperLink": "Sign in",
			"theTypeValue": "",
			"Nojive": "",
			"wosid": "@token"
		}
	}
}
