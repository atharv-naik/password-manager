keys = list("0123456789" + 
			"abcdefghijklmnopqrstuvwxyz" + 
			"ABCDEFGHIJKLMNOPQRSTUVWXYZ" +
			". @#_&-+()/*:;!?§÷|,~`'×¶£€$¢^={}\%[]"
			) # length 99


def base_99to10(num):
	base = len(keys)
	decimal_num = 0
	for i in range(len(num)):
		index = keys.index(num[i])
		apnd = (base ** (len(num) - i - 1)) * index
		decimal_num += apnd
	return int(decimal_num)


def base_10to99(num):
	base = len(keys)
	base96 = ""
	while True:
		if int(num // base) == 0:
			base96 = str(keys[int(num % base)]) + base96
			break

		base96 = str(keys[int(num % base)]) + base96
		num = num // base
	return base96
 

def Encrypt(string, key):
	key = str(key)
	key = base_99to10(key)
	num = base_99to10(string)
	encrypted_num = num * key
	encrypted = base_10to99(encrypted_num)

	return encrypted


def Decrypt(string, key):
	key = str(key)
	key = base_99to10(key)
	num = base_99to10(string)
	decrypted_num = int(num // key)
	decrypted = base_10to99(decrypted_num)

	return decrypted
