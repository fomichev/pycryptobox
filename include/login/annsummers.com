{
	"type":"login",
	"name": "Ann Summers",
	"address": "https://www.annsummers.com/webapp/wcs/stores/servlet/RegistrationLoginView?catalogId=10002&langId=-1&storeId=10151&krypto=vErwH6MNp5e9GF4U6QjEAq%2B45rgxOeVNtyZXiohTUZg%3D&ddkey=http:RegistrationLoginView",
	"form":
	{
		"action": "https://www.annsummers.com/webapp/wcs/stores/servlet/ESiteLogon",
		"method": "post",
		"fields":
		{
			"catalogId": "10002",
			"storeId": "10151",
			"reLogonURL": "RegistrationLoginView",
			"eSite": "Y",
			"successFlag": "true",
			"fromOrderId": "*",
			"toOrderId": ".",
			"deleteIfEmpty": "*",
			"URL": "OrderItemMove?page=&URL=OrderCalculate%3FURL%3DDashboardView&calculationUsageId=-1&calculationUsageId=-2&calculationUsageId=-7&shipModeId=",
			"signInLogonId": "",
			"logonId": "$username",
			"logonPassword": "$password",
			"eventId": "Login",
			"categoryId": "",
			"attr1": "REGISTRATION",
			"attr2": "Login Button Click",
			"attr4": "Commerce",
			"attr5": "2",
			"attr6": "0",
			"proceedSignIn": "Sign In"
		}
	}
}
