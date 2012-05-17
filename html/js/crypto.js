function decrypt(pass, salt, cipher, iterations, iv) {
//	var secret = CryptoJS.enc.Hex.parse("d0a62b0e861875dcb5a87eb45156adb385e7b776ba4c34ba78a97efec38256b4");
	var secret = CryptoJS.PBKDF2(pass, CryptoJS.enc.Base64.parse(salt), { keySize: 256/32, iterations: 1000 });
	var result = CryptoJS.AES.decrypt(cipher, secret, { mode: CryptoJS.mode.CBC, iv: CryptoJS.enc.Base64.parse(iv), padding: CryptoJS.pad.Pkcs7 });
	return result.toString(CryptoJS.enc.Utf8);
}
