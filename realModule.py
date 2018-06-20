def extendLen(string, length):
	while len(string) < length:
		string = "0" + string
	return string
def readToDict(fname):
	raw = open(fname).read().split("\n")
	retd = {}
	parity = 0
	key = None
	for val in raw:
		if parity:
			retd[key] = val
		else:
			key = val
		parity = 1-parity
	return retd
standardBlockList1 = ["@", "#", "(", ")", "\\", "/", "."]
standardBlockList2 = ["*", "\"", "[", "]", ":", ";", "|", "=", ","]
#
#
#
class thing():
	pass
#
#
#
class LoginEngine():
	def __init__(self):
		self.encryptVars = thing()
		self.loginVars = thing()
		self.dbVars = thing()
		self.registerVars = thing()
		self.dbVars.savedDatabase = None
		self.chngpswdVars = thing()
#
	def Encrypt(self, key, userName, passWord):
		if not(type(userName) == str and type(passWord) == str and type(key) == int):
			raise TypeError("Invalid argument(s) for Encrypt")
		self.encryptVars.result = None
		self.encryptVars.brokenPW = list(passWord)
		for x in range(0, len(passWord)):
			self.encryptVars.brokenPW[x] = ord(self.encryptVars.brokenPW[x]) * key * len(userName) * len(passWord)
			self.encryptVars.brokenPW[x] = extendLen(str(self.encryptVars.brokenPW[x]), 10)
		self.encryptVars.result = "".join(self.encryptVars.brokenPW)
#
	#you need to encrypt the password first, then pass it as an argument
	#by default uses the loaded data from text file as database, but you can use a custom one if necessary
	def Login(self, key, userName, passWord, **kwargs):
		if "db" in kwargs:
			dataBase = kwargs["db"]
		else:
			dataBase = self.dbVars.savedDatabase
		if not(type(key) == int and type(userName) == str and type(passWord) == str and type(dataBase) == dict):
			raise TypeError("Invalid argument(s) for Login")
		if userName in dataBase:
			if passWord == dataBase[userName]:
				self.loginVars.status = "SuccessfulLogin"
				self.loginVars.user = userName
				return
			else:
				self.loginVars.status = "IncorrectPassword"
				self.loginVars.user = None
				return
		else:
			self.loginVars.status = "UserDoesNotExist"
			self.loginVars.user = None
			return
#
	def LoadDataBase(self, dbName):
		if type(dbName) != str:
			raise TypeError("Invalid argument(s) for LoadDataBase")
		self.dbVars.savedDatabase = readToDict(dbName)
#
	def UpdateDataBase(self, filename):
		if type(filename) != str:
			raise TypeError("Invalid argument(s) for UpdateDataBase")
		self.dbVars.saveFile = open(filename, "w+")
		self.dbVars.saveFile.truncate(0)
		for x in self.dbVars.savedDatabase:
			self.dbVars.saveFile.write(x + "\n" + self.dbVars.savedDatabase[x] + "\n")
		self.dbVars.saveFile.close()
#
	def Register(self, userName, passWord, UNprohibited, PWprohibited, key):
		if not(type(userName) == str and type(passWord) == str and (type(UNprohibited) == str or type(UNprohibited) == list) and (type(PWprohibited) == str or type(PWprohibited) == list) and type(key) == int):
			raise TypeError("Invalid argument(s) for Register")
		for x in userName:
			if x in UNprohibited:
				self.registerVars.status = "InvalidCharInUsername"
				return
		for x in passWord:
			if x in PWprohibited:
				self.registerVars.status = "InvalidCharInPassword"
				return
		if userName in self.dbVars.savedDatabase:
			self.registerVars.status = "UsernameTaken"
			return
		self.Encrypt(key, userName, passWord)
		self.registerVars.status = "SuccesfulRegister"
		self.dbVars.savedDatabase[userName] = self.encryptVars.result
		self.Login(key, userName, passWord)
#
	#newPassWord should be encrypted, oldPassWord should not
	def ChangePassword(self, userName, oldPassWord, newPassWord, PWprohibited, key):
		if not(type(userName) == str and type(oldPassWord) == str and type(newPassWord) == str and (type(PWprohibited) == str or type(PWprohibited) == list)):
			raise TypeError("Invalid argument(s) for ChangePassword")
		for x in newPassWord:
			if x in PWprohibited:
				self.chngpswdVars.status = "InvalidCharInPassword"
				return
		if userName not in self.dbVars.savedDatabase:
			self.chngpswdVars.status = "UserDoesNotExist"
			return
		self.Encrypt(key, userName, oldPassWord)
		if self.encryptVars.result == self.dbVars.savedDatabase[userName]:
			self.dbVars.savedDatabase[userName] = newPassWord
			self.chngpswdVars.status = "SuccessfulPswdChng"
		else:
			self.chngpswdVars.status = "IncorrectOldPassword"
#
	def LogOut(self):
		if self.loginVars.user != None:
			self.loginVars.user = None
#
#
#
class LoginConsoleInteractivity(LoginEngine):
	def __init__(self, dataBase, UNrestrict, PWrestrict, key):
		super(LoginConsoleInteractivity, self).__init__()
		if not(type(dataBase) == dict and (type(UNrestrict) == str or type(UNrestrict) == list) and (type(PWrestrict) == str or type(PWrestrict) == list) and type(key) == int):
			raise TypeError("Invalid argument(s) for init of LCI")
		self.dbVars.savedDatabase = dataBase
		self.unique = thing()
		self.unique.key = key
		self.unique.mode = "blank"
		self.unique.unrest = UNrestrict
		self.unique.pwrest = PWrestrict
#
	def UseIn(self):
		print("Powered by hfble")
		while not(self.unique.mode.lower().startswith("l") or self.unique.mode.lower().startswith("r") or self.unique.mode.lower().startswith("q")):
			self.unique.mode = input("Do you want to log in, register, or quit?\nType in your choice and press enter.\n")
			if self.unique.mode.lower().startswith("l"):
				self.unique.realmode = "l"
			elif self.unique.mode.lower().startswith("r"):
				self.unique.realmode = "r"
			elif self.unique.mode.lower().startswith("q"):
				self.unique.realmode = "q"
			else:
				input("Invalid option. Try again.\n(Press enter to continue)")
		if self.unique.realmode == "l":
			self.loginVars.status = "blank"
			while self.loginVars.status != "SuccessfulLogin":
				self.unique.unin = input("Username:")
				self.unique.pwin = input("Password:")
				self.Encrypt(self.unique.key, self.unique.unin, self.unique.pwin)
				self.Login(self.unique.key, self.unique.unin, self.encryptVars.result)
				if self.loginVars.status == "UserDoesNotExist":
					input("User not found. Try again.\n(Press enter to continue)")
					print("\n" * 50)
				if self.loginVars.status == "IncorrectPassword":
					input("Incorrect password. Try again.\n(Press enter to continue)")
					print("\n" * 50)
			input("You have logged in as " + self.loginVars.user + "\n(Press enter to continue)")
		elif self.unique.realmode == "r":
			self.registerVars.status = "blank"
			while self.registerVars.status != "SuccesfulRegister":
				self.unique.unin = input("Username:")
				self.unique.pwin = input("Password:")
				self.Register(self.unique.unin, self.unique.pwin, self.unique.unrest, self.unique.pwrest, self.unique.key)			
				if self.registerVars.status == "InvalidCharInUsername":
					input("Invalid username.\n(Press enter to continue)")
					print("\n" * 50)
				elif self.registerVars.status == "InvalidCharInPassword":
					input("Invalid password.\n(Press enter to continue)")
					print("\n" * 50)
				if self.registerVars.status == "UsernameTaken":
					input("Someone already has that username.\n(Press enter to continue)")
					print("\n" * 50)
				if self.registerVars.status == "SuccesfulRegister":
					input("You have registered as "+ self.loginVars.user + "\n(Press enter to continue)")
				#I"M RIGHT HERE
		elif self.unique.realmode == "q":
			return
#
	def UseOut(self):
		print("Powered by hfble")
		self.unique.mode = input("Do you want to log out?")
		if self.unique.mode.startswith("y"):
			self.LogOut()
#
	def UseDuring(self):
		print("Powered by hfble")
		self.unique.mode = input("Do you want to change your password, log out, or quit?")
		if self.unique.mode.startswith("c"):
			self.chngpswdVars.status = "blank"
			while self.chngpswdVars.status != "SuccessfulPswdChng":
				self.unique.pwin = input("Old password:")
				self.unique.npwin1 = input("New password:")
				self.unique.npwin2 = input("Confirm new password:")
				if self.unique.npwin1 != self.unique.npwin2:
					input("New passwords do not match.\n(Press enter to continue)")
					print("\n" * 50)
					continue
				self.Encrypt(self.unique.key, self.loginVars.user, self.unique.npwin1)
				self.ChangePassword(self.loginVars.user, self.unique.pwin, self.encryptVars.result, self.unique.pwrest, self.unique.key)
				if self.chngpswdVars.status == "InvalidCharInPassword":
					input("Invalid password.\n(Press enter to continue)")
					print("\n" * 50)
				if self.chngpswdVars.status == "UserDoesNotExist":
					input("This message should not appear.\nIf it does, please contact HFB at weird1152@gmail.com.\n(Press enter to continue)")
					print("\n" * 50)
				if self.chngpswdVars.status == "IncorrectOldPassword":
					input("Incorrect old password.\n(Press enter to continue)")
					print("\n" * 50)
			input("Password successfully changed.\n(Press enter to continue)")
			print("\n" * 50)
		if self.unique.mode.startswith("l"):
			self.LogOut()
		if self.unique.mode.startswith("q"):
			return