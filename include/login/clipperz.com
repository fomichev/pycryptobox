{
	"type":"login",
	"name": "Clipperz",
	"address": "https://www.clipperz.com/beta/",
	"broken": "1",
	"form":
	{
		"action": "",
		"method": "get",
		"fields":
		{
			"username": "$name",
			"passphrase": "$password"
		}
	}
}
