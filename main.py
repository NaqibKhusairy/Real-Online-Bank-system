import mysql.connector
import bcrypt
import random

table = [
    [" 1", "Login"],
    [" 2", "ATM Function"],
    [" 3", "Forgot Password"],
    [" 4", "Staff Bank"]
]

table2 = [
    [" 1", "Login As Staff"],
    [" 2", "Forgot Staff Password"],
    [" 3", "Back"]
]

table3 = [
    [" 1", "Register New User"],
    [" 2", "Register New Staff"],
    [" 3", "Check User Account"],
    [" 4", "Deactivated Account"],
    [" 5", "activated Account"],
    [" 6", "Change Password"],
    [" 7", "Delete Account"],
    [" 8", "Check Money In All Account"],
    [" 9", "Log Out"]
]

table4 = [
    [" 1", "Register New User"],
    [" 2", "Check User Account"],
    [" 3", "Change Password"],
    [" 4", "Delete Account"],
    [" 5", "Check Money In All Account"],
    [" 6", "Log Out"]
]

def database():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="onlinebank")

def createdatabase():
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="")
        
        myprojectdb = mydb.cursor()
        myprojectdb.execute("CREATE DATABASE IF NOT EXISTS onlinebank")

        projectdatabase = database()
        mydbse = projectdatabase.cursor()

        mydbse.execute("CREATE TABLE IF NOT EXISTS user "
                       "(accountnum VARCHAR(12), "
                       "username VARCHAR(200), "
                       "password VARCHAR(200), "
                       "category VARCHAR(200),"
                       "active VARCHAR(200), "
                       "money DOUBLE,"
                       "PRIMARY KEY (accountnum))")

        mydbse.execute("CREATE TABLE IF NOT EXISTS stafbank "
                       "(username VARCHAR(200), "
                       "password VARCHAR(200), "
                       "category VARCHAR(200),"
                       "active VARCHAR(200), "
                       "PRIMARY KEY (username)) ")

        mydbse.execute("CREATE TABLE IF NOT EXISTS history "
                       "(username VARCHAR(200), "
                       "detail VARCHAR(200), "
                       "money VARCHAR(200)) ")

        try:
            projectdatabase = database()
            mydbse = projectdatabase.cursor()
            mydbse.execute("SELECT * FROM stafbank WHERE username=%s",
                           ("admin",))
            sameinpt = mydbse.fetchone()

            if not sameinpt:
                passwrd = "admin"
                passwrd = bcrypt.hashpw(passwrd.encode('utf-8'), bcrypt.gensalt())
                mydbse.execute("INSERT INTO stafbank"
                               "(username, password, category, active)"
                               "VALUES(%s, %s , %s, %s)",
                               ("admin", passwrd, "admin", "active"))
                projectdatabase.commit()

        except mysql.connector.Error as err:
            print("Failed to Insert data: {}".format(err))
    except mysql.connector.Error as err:
        print("Error: {}".format(err))

def unactive(username):
    print("\n-------------------------------------------------------------")
    print("                     Deactivated User Account")
    print("-------------------------------------------------------------\n")
    username2 = input("Please enter your Username: ")
    print("\n-------------------------------------------------------------")
    try:
        projectdatabase = database()
        mydbse = projectdatabase.cursor()
        
        mydbse.execute("SELECT * FROM user WHERE username=%s", (username2,))
        user_record = mydbse.fetchone()

        if user_record:
            mydbse.execute("SELECT * FROM stafbank WHERE username=%s", (username2,))
            staff_record = mydbse.fetchone()

            if staff_record:
                mydbse.execute("UPDATE stafbank SET active=%s WHERE username=%s",
                               ("inactive", username2))
                projectdatabase.commit()

            mydbse.execute("UPDATE user SET active=%s WHERE username=%s",
                           ("inactive", username2))
            projectdatabase.commit()
            
            print("Deactivated " + username2 + " account successfully")
            staff(username)
        else:
            print("User Not Found")

    except Exception as e:
        print("Failed to Deactivate User:", str(e))
        staff(username)

def activeacc(username):
    print("\n-------------------------------------------------------------")
    print("                     Activate User Account")
    print("-------------------------------------------------------------\n")
    username2 = input("Please enter your Username: ")
    print("\n-------------------------------------------------------------")
    try:
        projectdatabase = database()
        mydbse = projectdatabase.cursor()
        
        mydbse.execute("SELECT * FROM user WHERE username=%s", (username2,))
        user_record = mydbse.fetchone()

        if user_record:
            mydbse.execute("SELECT * FROM stafbank WHERE username=%s", (username2,))
            staff_record = mydbse.fetchone()

            if staff_record:
                mydbse.execute("UPDATE stafbank SET active=%s WHERE username=%s",
                               ("active", username2))
                projectdatabase.commit()

            mydbse.execute("UPDATE user SET active=%s WHERE username=%s",
                           ("active", username2))
            projectdatabase.commit()
            
            print("Activated " + username2 + " account successfully")
            staff(username)
        else:
            print("User Not Found")

    except Exception as e:
        print("Failed to Activated User:", str(e))
        staff(username)

def checkuser(username):
    print("\n-------------------------------------------------------------")
    print("                     Check User Account")
    print("-------------------------------------------------------------\n")
    username2 = input("Please enter your Username: ")
    print("\n-------------------------------------------------------------")
    try:
        projectdatabase = database()
        mydbse = projectdatabase.cursor()
        mydbse.execute("SELECT * FROM user WHERE username=%s",(username2,))
        sameinpt = mydbse.fetchone()

        if sameinpt:
            mydbse.execute("SELECT accountnum FROM user WHERE username=%s",
                           (username2,))
            accountnum = mydbse.fetchone()[0]

            mydbse.execute("SELECT category FROM user WHERE username=%s",
                           (username2,))
            category = mydbse.fetchone()[0]

            mydbse.execute("SELECT active FROM user WHERE username=%s",
                           (username2,))
            activate = mydbse.fetchone()[0]

            mydbse.execute("SELECT money FROM user WHERE username=%s",
                           (username2,))
            money = mydbse.fetchone()[0]

            print("Account Number : "+accountnum)
            print("Username : "+username2)
            print("Category : "+category)
            print("Account Balance : RM {:.2f}".format(money))
            print("Acount is : "+activate)
            staff(username)
        else:
            print("User Not Found")

    except :
        print("Failed to Find User ")
        staff(username)


def registerstaff(username):
    accountnum = ''.join(str(random.randint(0, 9)) for _ in range(12))
    try:
        projectdatabase = database()
        mydbse = projectdatabase.cursor()
        mydbse.execute("SELECT * FROM user WHERE accountnum=%s",
                       (accountnum,))
        sameinpt = mydbse.fetchone()

        if not sameinpt:
            username2 = input("Please enter Username: ")
            mydbse.execute("SELECT * FROM user WHERE username=%s",
                           (username2,))
            sameinpt = mydbse.fetchone()

            if sameinpt:
                print("The Account is Already Registered.")
                askuser=input("Do you want To Register Other Account ? [ Y to continue or any key to back] : ")
                askuser=askuser.upper()
                if askuser == "Y":
                    registerstaff(username)
                else :
                    staff(username)
            else:
                mydbse.execute("SELECT * FROM stafbank WHERE username=%s",
                               (username2,))
                sameinpt = mydbse.fetchone()
                if sameinpt:
                    print("The Account is Already Registered.")
                    askuser=input("Do you want To Register Other Account ? [ Y to continue or any key to back] : ")
                    askuser=askuser.upper()
                    if askuser == "Y":
                        registerstaff(username)
                    else :
                        staff(username)
                else:
                    category=input("Please enter the owner was staff or admin : ")
                    category= category.lower()
                    if category =="staff" or category == "admin":
                        passwrd = "123"
                        passwrd = bcrypt.hashpw(passwrd.encode('utf-8'), bcrypt.gensalt())
                        money = 10
                        activate="active"
                        mydbse.execute("INSERT INTO user"
                                       "(accountnum, username, password, category, active, money)"
                                       "VALUES(%s, %s, %s, %s, %s, %s)",
                                       (accountnum,username2, passwrd,category,activate, money))
                        projectdatabase.commit()

                        mydbse.execute("INSERT INTO history"
                                       "(username, detail, money)"
                                       "VALUES(%s, %s, %s)",
                                       (username2, "Register Account", "+RM {:.2f}".format(money)))
                        projectdatabase.commit()

                        mydbse.execute("INSERT INTO stafbank"
                                       "(username, password, category, active)"
                                       "VALUES(%s, %s, %s, %s)",
                                       (username2, passwrd,category,"active"))
                        projectdatabase.commit()

                        print("Staff Registeration Complete ....")
                        print("Account Number : "+accountnum+
                            "\nUsername : "+username2+
                            "\nPassword : "+"123"+
                            "\nCategory : "+category+
                            "\nAmount In Account : "+"RM {:.2f}".format(money))
                        staff(username)
                    else:
                        print("You just need to fill either admin or staff only !!!! \nPlease register again !!!!")
                        registeruser(username)
        else :
            registerstaff(username)

    except mysql.connector.Error as err:
        print("Failed to Insert data: {}".format(err))

def registeruser(username):
    accountnum = ''.join(str(random.randint(0, 9)) for _ in range(12))
    try:
        projectdatabase = database()
        mydbse = projectdatabase.cursor()
        mydbse.execute("SELECT * FROM user WHERE accountnum=%s",
                       (accountnum,))
        sameinpt = mydbse.fetchone()

        if not sameinpt:
            username2 = input("Please enter Username: ")
            mydbse.execute("SELECT * FROM user WHERE username=%s",
                           (username2,))
            sameinpt = mydbse.fetchone()

            if sameinpt:
                print("The Account is Already Registered.")
                askuser=input("Do you want To Register Other Account ? [ Y to continue or any key to back] : ")
                askuser=askuser.upper()
                if askuser == "Y":
                    registeruser(username)
                else :
                    staff(username)
            else:
                passwrd = "123"
                passwrd = bcrypt.hashpw(passwrd.encode('utf-8'), bcrypt.gensalt())
                money = 10
                activate = "active"
                category = "user"
                mydbse.execute("INSERT INTO user"
                               "(accountnum, username, password, category, active, money)"
                               "VALUES(%s, %s, %s, %s, %s, %s)",
                               (accountnum,username2, passwrd,category,activate, money))
                projectdatabase.commit()

                mydbse.execute("INSERT INTO history"
                               "(username, detail, money)"
                               "VALUES(%s, %s, %s)",
                               (username2, "Register Account", "+RM {:.2f}".format(money)))
                projectdatabase.commit()

                print("Registeration Complete ....")
                print("Account Number : "+accountnum+
                    "\nUsername : "+username2+
                    "\nPassword : "+"123"+
                    "\nAmount In Account : "+"RM {:.2f}".format(money))
                staff(username)
        else :
            registeruser(username)

    except mysql.connector.Error as err:
        print("Failed to Insert data: {}".format(err))

def staff(username):
    count=3
    try:
        projectdatabase = database()
        mydbse = projectdatabase.cursor()
        mydbse.execute("SELECT category FROM stafbank WHERE username=%s",
                       (username,))
        user_data = mydbse.fetchone()
        print("\n-------------------------------------------------------------")
        print("          "+user_data[0].lower()+" Username: "+username)
        print("-------------------------------------------------------------\n")
        if user_data[0].lower() == "admin":
            for row in table3:
                for col in row:
                    print(col, end="\t")
                print()
            print("-------------------------------------------------------------")

            try:
                userchoice = int(input("Please Choose [1 or 2 or 3 or 4 or 5 or 6 or 7 or 8 or 9]: "))
                if userchoice == 1 or userchoice == 2:
                    if userchoice == 1:
                        print("\n-------------------------------------------------------------")
                        print("                         User Register")
                        print("-------------------------------------------------------------\n")
                        registeruser(username)
                    elif userchoice == 2:
                        registerstaff(username)
                elif userchoice == 3:
                    checkuser(username)
                elif userchoice == 4:
                    unactive(username)
                elif userchoice == 5:
                    activeacc(username)
                elif userchoice == 6:
                    print("belum siap")
                elif userchoice == 7:
                    print("belum siap")
                elif userchoice == 8:
                    print("belum siap")
                elif userchoice == 9:
                    admin(count)
                else:
                    print("\n-------------------------------------------------------------\n")
                    print("     You just need to fill either 1 or 2 or 3 or 4 or 5 or 6 or 7 or 8 or 9 !!!")
                    print("\n-------------------------------------------------------------\n")
            except ValueError:
                print("\n-------------------------------------------------------------\n")
                print("     You just need to fill either 1 or 2 or 3 or 4 or 5 or 6 or 7 or 8 or 9 !!!")
                print("\n-------------------------------------------------------------\n")

        else:
            for row in table4:
                for col in row:
                    print(col, end="\t")
                print()
            print("-------------------------------------------------------------")

            try:
                userchoice = int(input("Please Choose [1 or 2 or 3 or 4 or 5 or 6 ]: "))
                if userchoice == 1 or userchoice == 2:
                    if userchoice == 1:
                        print("\n-------------------------------------------------------------")
                        print("                         User Register")
                        print("-------------------------------------------------------------\n")
                        registeruser(username)
                    elif userchoice == 2:
                        checkuser(username)
                elif userchoice == 3:
                    print("belum siap")
                elif userchoice == 4:
                    print("belum siap")
                elif userchoice == 5:
                    print("belum siap")
                elif userchoice == 6:
                    admin(count)
                else:
                    print("\n-------------------------------------------------------------\n")
                    print("     You just need to fill either 1 or 2 or 3 or 4 or 5 or 6 !!!")
                    print("\n-------------------------------------------------------------\n")
            except ValueError:
                print("\n-------------------------------------------------------------\n")
                print("     You just need to fill either 1 or 2 or 3 or 4 or 5 or 6 !!!")
                print("\n-------------------------------------------------------------\n")

        print("belum siap")

    except mysql.connector.Error as err:
        print("Failed to determine user category: {}".format(err))

def staffforgotpassword():
    print("\n-------------------------------------------------------------")
    print("                    Staff Forgot Password")
    print("-------------------------------------------------------------\n")
    username = input("Please enter your Username: ")

    try:
        projectdatabase = database()
        mydbse = projectdatabase.cursor()
        mydbse.execute("SELECT * FROM stafbank WHERE username=%s",
                       (username,))
        user_data = mydbse.fetchone()

        if user_data:
            passwrd = input("Please enter your New Password: ")
            cpasswrd = input("Please confirm your New Password: ")

            if passwrd == cpasswrd : 
                passwrd = bcrypt.hashpw(passwrd.encode('utf-8'), bcrypt.gensalt())
                mydbse.execute("UPDATE stafbank SET password=%s WHERE username=%s",
                    (passwrd, username))
                projectdatabase.commit()
                print("Welcome back, " + username + ".")
                staff(username)
            else :
                print("Please Make Sure Your Password and confirm passwrd is same. please register again")
                staffforgotpassword()
        else:
            print("Your account is not in the database, please register first")
            askuser=input("Do you want To bank ? [ Y to back or any key to continue ] : ")
            askuser=askuser.upper()
            if askuser == "Y":
                print()
                admin(count)
            else :
                staffforgotpassword()

    except mysql.connector.Error as err:
        print("Failed to log in: {}".format(err))

def loginstaf(count):
    print("\n-------------------------------------------------------------")
    print("                          Staff Log In")
    print("-------------------------------------------------------------\n")
    username = input("Please enter your Username: ")

    try:
        projectdatabase = database()
        mydbse = projectdatabase.cursor()
        mydbse.execute("SELECT * FROM stafbank WHERE username=%s",
                       (username,))
        user_data = mydbse.fetchone()

        if user_data:
            mydbse.execute("SELECT active FROM stafbank WHERE username=%s",
                           (username,))
            user_data2 = mydbse.fetchone()
            if user_data2[0].lower() == "active" : 
                passwrd = input("Please enter your Password: ")
                if bcrypt.checkpw(passwrd.encode('utf-8'), user_data[1].encode('utf-8')):
                    print("Welcome back, " + username + ".")
                    staff(username)
                else:
                    if count == 1:
                        print("Your password is wrong. Sorry You have reached the Maximum Limit which is 3 times. Please Try Again")
                        print("\n-------------------------------------------------------------")
                        admin(3)
                    else:
                        count -= 1
                        print("Your password is wrong. Please try again. You only have " + str(count) + " chances left")
                        loginstaf(count)
            else:
                print("Your Account Is unactive ... Please Contact Your Bank..")
        else:
            print("Your staff account is not in the database, are you serious you are staff?")
            askuser = input("Do you want To Login Y for yes or any key to quit ? [ Y or any key ] : ")
            askuser = askuser.upper()
            if askuser == "Y":
                loginstaf(count)
            else:
                print("\n-------------------------------------------------------------")
                admin(3)

    except mysql.connector.Error as err:
        print("Failed to log in: {}".format(err))

def admin(count):
    print("\n-------------------------------------------------------------")
    print("                          Staff Bank")
    print("-------------------------------------------------------------")
    for row in table2:
        for col in row:
            print(col, end="\t")
        print()
    print("-------------------------------------------------------------")
    
    try:
        userchoice = int(input("Please Choose [1 or 2 or 3]: "))
        if userchoice == 1 or userchoice == 2:
            if userchoice == 1:
                loginstaf(count)
            elif userchoice == 2:
                staffforgotpassword()
        elif userchoice == 3:
            choose()
        else:
            print("\n-------------------------------------------------------------\n")
            print("     You just need to fill either 1 or 2 or 3 !!!")
            print("\n-------------------------------------------------------------\n")
    except ValueError:
        print("\n-------------------------------------------------------------\n")
        print("     You just need to fill either 1 or 2 or 3 !!!")
        print("\n-------------------------------------------------------------\n")

def user(username):
    print("User functionality for user", username)

def login(count):
    print("\n-------------------------------------------------------------")
    print("                             Log In")
    print("-------------------------------------------------------------\n")
    username = input("Please enter your Username: ")

    try:
        projectdatabase = database()
        mydbse = projectdatabase.cursor()
        mydbse.execute("SELECT * FROM user WHERE username=%s",
                       (username,))
        user_data = mydbse.fetchone()

        if user_data:
            mydbse.execute("SELECT active FROM user WHERE username=%s",
                           (username,))
            user_data2 = mydbse.fetchone()
            if user_data2[0].lower() == "active" : 
                passwrd = input("Please enter your Password: ")
                if bcrypt.checkpw(passwrd.encode('utf-8'), user_data[2].encode('utf-8')):
                    print("Welcome back, " + username + ".")
                    user(username)
                else:
                    if count == 1:
                        print("Your password is wrong. Sorry You have reached the Maximum Limit which is 3 times. Please Try Again")
                        print("\n-------------------------------------------------------------")
                        choose()
                    else:
                        count -= 1
                        print("Your password is wrong. Please try again. You only have " + str(count) + " chances left")
                        login(count)
            else:
                print("Your Account Is unactive ... Please Contact Your Bank..")
        else:
            print("Your account is not in the database, please register at the bank first")
            askuser = input("Do you want To Login Y for yes or any key to quit ? [ Y or any key ] : ")
            askuser = askuser.upper()
            if askuser == "Y":
                login(count)
            else:
                print("\n-------------------------------------------------------------")
                choose()

    except mysql.connector.Error as err:
        print("Failed to log in: {}".format(err))

def choose():
    count = 3
    for row in table:
        for col in row:
            print(col, end="\t")
        print()
    print("-------------------------------------------------------------")
    
    try:
        userchoice = int(input("Please Choose [1 or 2 or 3 or 4]: "))
        print()
        if userchoice == 1 or userchoice == 2:
            if userchoice == 1:
                login(count)
            elif userchoice == 2:
                print("ATM Function not implemented yet")
        elif userchoice == 3:
            print("Forgot Password not implemented yet")
        elif userchoice == 4:
            admin(count)
        else:
            print("\n-------------------------------------------------------------\n")
            print("     You just need to fill either 1 or 2 or 3 or 4 !!!")
            print("\n-------------------------------------------------------------\n")
    except ValueError:
        print("\n-------------------------------------------------------------\n")
        print("     You just need to fill either 1 or 2 or 3 or 4 !!!")
        print("\n-------------------------------------------------------------\n")

createdatabase()

print("-------------------------------------------------------------")

while True:
    choose()
