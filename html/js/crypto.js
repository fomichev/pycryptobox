function decrypt(pass, salt, cipher, iterations, mode, iv) {
	var pbk = Crypto.PBKDF2(pass, Crypto.util.hexToBytes(salt), 32, { iterations: iterations });
	var secret = Crypto.util.hexToBytes(pbk);
	var text = Crypto.util.base64ToBytes(cipher);

	return Crypto.AES.decrypt(text, secret, { mode: mode, iv: Crypto.util.hexToBytes(iv) });
}
