import base64
import hashlib
import random
import time

from data.constants import SPECIAL_CHARACTERS


def addSpecialCharacters(encodedStr):
	charList = list(encodedStr)
	numSpecialChars = min(6, len(encodedStr))

	for i in range(numSpecialChars):
		index = (i * 7) % len(charList)
		charList[index] = SPECIAL_CHARACTERS[i % len(SPECIAL_CHARACTERS)]

	return ''.join(charList)


def calculateCipher(userData, user):
	userId = (abs(user.id) % 1000)
	userIdStr = str(userId)
	if len(set(userIdStr)) == 1:
		userId = userId + 194
	elif userId < 100:
		userId = userId * 6 + 100

	userData['passes'] = len(userData['cipher'] * userData['length']) + userId - 6
	userData['salt'] = userData['cipher'][1] + str(user.id + ((len(userData['cipher']) + 6) * 6)) + userData['cipher'][
		-1]

	md5Hash = bytes(userData['cipher'], 'utf-8')
	for _ in range(userData['passes']):
		md5Hash = hashlib.md5(md5Hash).digest()

	pbkdf2Hash = hashlib.pbkdf2_hmac('sha256', md5Hash, bytes(userData['salt'], 'utf-8'), userData['passes'])
	base64EncodedHash = base64.b64encode(pbkdf2Hash).decode('utf-8')
	diverseEncodedHash = addSpecialCharacters(base64EncodedHash)

	finalHash = 'S' + diverseEncodedHash[1:userData['length'] - 1] + 'Y'

	finalHash = finalHash.replace("I", SPECIAL_CHARACTERS[int(str(userId)[-2])])
	finalHash = finalHash.replace("l", SPECIAL_CHARACTERS[int(str(userId)[-3])])
	finalHash = finalHash.replace("O", SPECIAL_CHARACTERS[int(str(userId)[-1])])

	return finalHash


def calculateRandomCipher():
	listToRandomize = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890#@+-_'!^.?abcdefghijklmnopqrstuvwxyz")
	random.shuffle(listToRandomize)
	cipher = ''.join(listToRandomize)[:random.randint(20, 45)]
	random.shuffle(listToRandomize)
	salt = ''.join(listToRandomize)[:random.randint(5, 10)] + str(time.time())

	md5Hash = bytes(cipher, 'utf-8')
	for _ in range(random.randint(50, 1000)):
		md5Hash = hashlib.md5(md5Hash).digest()

	pbkdf2Hash = hashlib.pbkdf2_hmac('sha256', md5Hash, bytes(salt, 'utf-8'), random.randint(50, 2024))
	base64EncodedHash = base64.b64encode(pbkdf2Hash).decode('utf-8')
	diverseEncodedHash = addSpecialCharacters(base64EncodedHash)

	finalHash = diverseEncodedHash[:random.randint(15, 45)]

	finalHash = finalHash.replace("I", SPECIAL_CHARACTERS[random.randint(0, 9)])
	finalHash = finalHash.replace("l", SPECIAL_CHARACTERS[random.randint(0, 9)])
	finalHash = finalHash.replace("O", SPECIAL_CHARACTERS[random.randint(0, 9)])

	return finalHash
