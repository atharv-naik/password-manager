# Welcome to Password Manager

import authenticate as auth
from dencrypt import Encrypt as encrypt
from dencrypt import Decrypt as decrypt
import getpass
import shutil
import time



SEPERATION = "•"
logged_in = 0
username = None
user_email = None

SIZE = shutil.get_terminal_size().columns


load2 = list("/-\|")
load = [".  ", ".. ", "...", "   "]


def align_center(s):
    return s.center(SIZE)


def loading(i, type=1):
    if type == 1:
        time.sleep(0.2)
        return load2[i%len(load2)]
    else:
        time.sleep(0.5)
        return load[i%len(load)]




def main():

    def check_key(val="Enter", adv=0):
        if not adv:
            key = getpass.getpass(f"{val} the Key\n-->")
            cnf_key = getpass.getpass("Confirm Key\n-->")
            if key == cnf_key:
                return key, True
            else:
                print("Keys dont match.")
                return key, False
        else:
            while True:
                prev_key = getpass.getpass("Previous Key --> ")
                new_key = getpass.getpass("New Key --> ")
                if new_key == prev_key:
                    print("New Key cannot be same as Previous Key")
                    continue
                cnf_key = getpass.getpass("Confirm Key --> ")
                if cnf_key != new_key:
                    print("New Key and Confirm Key do not match")
                    continue
                else:
                    return prev_key, new_key


    def delete(username):
        try:
            with open(f"pswds/.passwords_{username}", "r") as f:
                KEY = getpass.getpass('Enter the Key\n-->')
                pswd = f.read().split(SEPERATION)

            pswd.remove(pswd[len(pswd) - 1])

            passwords = []
            for pswd in pswd:
                pswd = decrypt(pswd, KEY)
                passwords.append(pswd)
            for i in range(len(passwords)):
                print(i+1, passwords[i])

            print('Enter the index of password to delete')
            offset = 0
            while True:
                inpt = input('-->')
                if inpt == 'Done':
                    break

                else:
                    del_index = int(inpt)
                    offset += 1
                    try:
                        passwords.remove(passwords[del_index - 1])
                    except:
                        passwords.remove(passwords[del_index - 1 - offset])    

            with open(f"pswds/.passwords_{username}", "w+") as f:
                for pswd in passwords:
                    pswd = encrypt(pswd, KEY) + SEPERATION
                    f.write(pswd)
            print("Password(s) deleted successfully.")
        except FileNotFoundError:
            print("You have not added any passwords yet. Type 'add' (a) to add one.")
        except:
            print("Something went wrong...")
            return


    def update(username):
        try:
            with open(f"pswds/.passwords_{username}", "r") as f:
                KEY = getpass.getpass('Enter the Key\n-->')
                pswd = f.read().split(SEPERATION)

            pswd.remove(pswd[len(pswd) - 1])

            passwords = []
            for pswd in pswd:
                pswd = decrypt(pswd, KEY)
                passwords.append(pswd)
            for i in range(len(passwords)):
                print(i+1, passwords[i])

            print('Enter the index of password to change and type "Done" to save changes')
            while True:
                inpt = input('-->')
                if inpt == 'Done':
                    break

                else:
                    incorrect_pswd = 1
                    while incorrect_pswd:
                        del_index = int(inpt)
                        print("New password")
                        new_pswd = getpass.getpass('-->')
                        print("Confirm password")
                        confirm_pswd = getpass.getpass("-->")
                        if new_pswd == confirm_pswd:
                            passwords[del_index - 1] = new_pswd
                            incorrect_pswd = 0
                        else:
                            print("Entered passwords dont match!")

            with open(f"pswds/.passwords_{username}", "w+") as f:
                for pswd in passwords:
                    pswd = encrypt(pswd, KEY) + SEPERATION
                    f.write(pswd)
            print("Passwords changed successfully")
        except FileNotFoundError:
            print("You have not added any passwords yet. Type 'add' (a) to add one.")
        except:
            print('Something went wrong...')
            return


    def add(username):
        with open(f"pswds/.passwords_{username}", "a") as f:
            KEY, ok = check_key(val='Set')
            if ok:
                print("Enter the password(s) you want to store\nType 'Done' command when you are done entering.")
                while True:
                    pswd = input()
                    if pswd == 'Done':
                        break
                    else:
                        pswd = encrypt(pswd, KEY)
                        f.write(pswd + SEPERATION)
            else:
                return
        print("Passwords added successfully")


    def view(username):
        try:
            with open(f"pswds/.passwords_{username}", "r") as f:
                KEY = getpass.getpass('Enter the Key\n-->')
                pswd = f.read().split(SEPERATION)
                if not len(pswd):
                    print("(no passwords to show)")
                    return

                pswd.remove(pswd[len(pswd) - 1])

                passwords = []
                for pswd in pswd:
                    pswd = decrypt(pswd, KEY)
                    passwords.append(pswd)

                for i in range(len(passwords)):
                    print(i+1, passwords[i])
        except FileNotFoundError:
            print("You have not added any passwords yet. Type 'add' (a) to add one.")


    def change_key(username):
        try:
            prev_key, new_key = check_key(adv=1)

            with open(f"pswds/.passwords_{username}", "r") as f:
                pswd = f.read().split(SEPERATION)

            pswd.remove(pswd[len(pswd) - 1])

            with open(f"cache/tmp_{username}", "w") as f:
                for pswd in pswd:
                    f.write(encrypt(decrypt(pswd, prev_key), new_key) + SEPERATION)
            with open(f"cache/tmp_{username}", "r") as f:
                content = f.read()
            with open(f"pswds/.passwords_{username}", "w") as f:
                f.write(content)
            with open(f"cache/tmp_{username}", "w") as f:
                null = ""
                f.write(null)
                return
        except:
            print("Something went wrong")


    def email(username, extention):
        if extention == '':
            extention = 'gmail.com'
        email = username + '@' + extention
        return email


    def login(after_logout=0):
        global logged_in
        global username
        global user_email

        if after_logout:
            logged_in = 0
            print(f"{username} logged out successfully\n")

        if not logged_in:
            print("Login to your account")
            username = input('Username: ').lower()
            extention = input('Email extention (skip if gmail account):\n-->')
            user_email = email(username, extention)
            logged_in = auth.execute(user_email)
            if logged_in:
                print(
                    "Type 'view' (v), 'add' (a), 'update' (u) or 'delete' (d) commands to view, add, change or delete passwords. Type 'Quit' (Q) command to exit.\nFor more information about commands type 'Help'."
                )
            return logged_in
        return 1


    def erase(username):
        print(
            f'This will permanently ERASE ALL the stored passwords for {username} account.\nThis action CANNOT be undone.')
        response = input("Do you want to continue? [Y/n] --> ")
        if response.lower() == 'y':
            print("Please wait...")
            authorized = auth.execute(user_email)
            if authorized:
                with open(f"pswds/.passwords_{username}", "w") as f:
                    null = ""
                    f.write(null)
                    print("All your passwords erased")
            else:
                print("Could not authenticate")
        else:
            print("Aborted.")
            return


    def helper():
        print(
            "All the Commands are summarised below—"
        )
        print(
            "add (a) - Adds new passwords\nview (v) - To view existing passwords\nupdate (u) - To update existing passwords\ndelete (d) - Deletes existing password(s) at a specified index\nchange_key - changes the key used to encrypt existing passwords (NOTE - previous key IS required for this process)"
        )
        print(
            "Quit (Q) - Exits the loop\nlogout - To logout of current account\nDone - Use after adding new passwods to a user account and after selecting existing passwords to delete from a user account\nErase - Deletes all existing passwords from a user account"
        )
        print(
            "Help - Summarises all the Commands to use password_manager"
        )


    def manage():
        global logged_in
        global username

        print(align_center("Welcome to password_manager\n"))
        print("="*shutil.get_terminal_size().columns + "\n")
        print(
            align_center("Manage all your passwords with ease!\n\n")
        )

        if login():
            while logged_in:
                original_inpt = input('-->')
                user_inpt = original_inpt.lower()[0]

                if user_inpt == 'v':
                    view(username)
                    continue


                elif user_inpt == 'a':
                    add(username)
                    continue


                elif user_inpt == 'u':
                    update(username)


                elif user_inpt == 'd':
                    delete(username)


                elif original_inpt == 'Erase':
                    erase(username)


                elif original_inpt == "change_key":
                    change_key(username)
                    

                elif original_inpt.lower() == 'logout':
                    login(after_logout=1)
                    continue


                elif original_inpt == 'Help':
                    helper()


                elif original_inpt == 'Quit' or original_inpt == 'Q':
                    print("Exiting..")
                    break

    manage()


if __name__ == "__main__":
    main()
