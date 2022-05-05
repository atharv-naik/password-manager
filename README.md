# password-manager
This is a command line interface that lets you store an encrypted copy your passwords locally using one master-password. 
Store an encrypted copy of your passwords and decrypt using one master-password.

# Installation
This script runs on `python3`.
Clone this repo or download the source code, and navigate to that directory and create two empty folders `pswds` and `cache`. For the script to work you need to generate an App password for mail client [here](https://www.youtube.com/redirect?event=video_description&redir_token=QUFFLUhqbDRJbE00YW95UUNkWFVfOFFvRloyejNna1VpZ3xBQ3Jtc0ttYThIUk01LUpBUFFuSkRkUEo1QlMyM2I1NGdhdjJoeE1aMUJ0TXRSNHdKZGRhRVNLWWt5cm1lYTQxSC1NM2NVN05KaHU2YkRZcGc4OFd3elpYYjdWSUFEWHlUODh1b0hUZGJGTmlYdHo5UVNHU2JtZw&q=https%3A%2F%2Fmyaccount.google.com%2Fapppasswords&v=JRCJ6RtE3xU) (You need to turn on 2-Step Verification for your google account for this). Add this password to the system environment variables with variable name set as `PASSWORD` and add another variable `EMAIL` to add the corresponding email address. You can now run the `main.py` file from the `terminal` and start using `password-manager`!

### Note
- You will be prompted to give an OTP sent on your gmail or any other email account each time you run the script for security reasons.
- Your master-password is not saved anywhere in any form.
- This is a fun project and the encryption-decryption algorithms were designed from scratch without using any external encrytion libraries and thus CANNOT guarentee perfection and vulnerabilities may be found.
