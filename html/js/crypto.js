function decrypt(pass, salt, cipher) {
	var pbk = Crypto.PBKDF2(pass, salt, 32, { iterations: 1000 });
	var secret = Crypto.util.hexToBytes(pbk);
	var text = Crypto.util.base64ToBytes(cipher);

	return Crypto.AES.decrypt(text, secret, { mode: new Crypto.mode.CFB });
}
