hfble v1.0
A Login API

Classes:

	LoginEngine()

		Is the basic data management system.
		Methods:
			__init__()
				Sets up some variables
			Encrypt(int key, str userName, str passWord)
				Sets self.encryptVars.result to an encrypted form of the passWord
			Login(int key, str userName, str passWord (encrypted), kwdict db)
				If db is given, this method will use what is passed in db as the database, otherwise it will use self.dbVars.savedDatabase
				This method simulates logging in, setting self.loginVars.user and self.loginVars.status
				self.loginVars.status will be set to one of the self-explanatory string values upon executing the function:
				"SuccessfulLogin"
				"IncorrectPassword"
				"UserDoesNotExist"
			LoadDataBase(str dbName)
				Reads from the file with the name provided by dbName, assuming it is a text file, and turns the information in the file into a dictionary, in which each odd-numbered line is a key and each even-numbered line is a value, storing the dictionary in self.dbVars.savedDatabase
			UpdateDataBase(str filename)
				Saves the data in self.dbVars.savedDatabase into the file with the name provided by filename, assuming it is a text file, storing the information in a similar format as what is described in LoadDataBase.
			Register(str userName, str passWord, str/list UNprohibited, str/list PWprohibited, int key)
				Adds an entry into self.dbVars.savedDatabase with the key of userName and the value of an encrypted form of passWord. It returns a self-explanatory string in self.registerVars.status from the following list:
				"InvalidCharInUsername"
				"InvalidCharInPassword"
				"UsernameTaken"
				"SuccessfulRegister"
			ChangePassword(str userName, str oldPassWord, str newPassWord (encrypted), str/list PWprohibited, int key)
				Changes the value for self.dbVars.savedDatabase[userName], and returns a self-explanatory string into self.chngpswdVars.status from the following list:
				"InvalidCharInPassword"
				"UserDoesNotExist"
				"SuccessfulPswdChng"
				"IncorrectOldPassword"
			LogOut()
				If self.loginVars.user is not None (someone is logged in), it will set it to None (log out).

	LoginConsoleInteractivity(LoginEngine)

		Uses LoginEngine to have an interface in the console/stdio.
		Methods:
			Inherited methods from LoginEngine - see above
			__init__(dict dataBase, str/list UNrestrict, str/list PWrestrict, int key)
				Sets up some variables, using the provided values.
			UseIn()
				Runs an interface for logging in and registering.
			UseOut()
				Gives the user an option to log out.
			UseDuring()
				Runs an interface for changing password and logging out.

	thing()

		A blank class. Used in the __init__ functions of the other classes.

Functions:

	extendLen(str string, int length)
		Returns the string, but extended with 0s at the beginning, exactly enough 0s such that the length of the return string is equal to the length argument.
	readToDict(str fname)
		Reads the file with the name provided by fname, assuming it is a text file, and converts it into a dictionary, in which each odd-numbered line is a key and each even-numbered line right after each odd-numbered line is the value for that key. It returns the dictionary.

Built-in variables:

	standardBlockList1(list)
		Is an example for UN/PW prohibit/restrict variables/arguments.
		It is a list of characters that would likely not be allowed in a username or password.
		Initially has the value of ["@", "#", "(", ")", "\\", "/", "."].
	standardBlockList2(list)
		Is an example for UN/PW prohibit/restrict variables/arguments.
		It is a list of characters that would likely not be allowed in a username or password.
		Initially has the value of ["*", "\"", "[", "]", ":", ";", "|", "=", ","].
