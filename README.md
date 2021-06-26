# MFA authentication using OTP and Google Authenticator

### Installation

If using anaconda create the new environment and activate it using

`conda create -n mfa python=3.8`
`conda activate mfa`

Clone the repo using git bash:

`git clone https://github.com/ry16-stern/freestyle.git`

Navigate to Freestyle folder and run the package installation command

`pip install -r requirements.txt`

You will need to create the .env file in the root folder of the project with your firebase configuration

The structure of the .env as follows

	apiKey= "Your apiKey"
	authDomain="YourauthDomain"
	projectId="Your projectId"
	storageBucket="Your storageBucket"
	messagingSenderId= "Your messagingSenderId"
	appId="Your appId"
	measurementId="Your measurementId"
	databaseURL="Your databaseURL"

to launch the app run

`python mfa.py`

There is a chance that Windows-based installation can run into errors with the Crypto package.
error: Python Tests: No module named 'Crypto'
The solution to this issue is to rename crypto folder in site-packages location from "crypto" to "Crypto" (Capital C)

To find the location of your site-packages run:

`python -m site`

Usually, site-packages are installed in the anaconda3 folder in

`C:\Users\[your username]\anaconda3\envs\mfa\lib\site-packages`

Rename crypto folder to Crypto and try running the app again.

#App workflow

## Registration

The user enters email and password.
The app passes it to firebase which creates the user account and gives back the token.
App uses the token id and passes it to RealTime Database.
The App generates a secret encrypted key and stores it with the unique id in the RealTimeDatabase for future reference.
The next step is the creation of the provisioning URI for the OTP app.
The app accepts the URI in the form QR code so the app generates one.
The app passes URI to the QR code generator and presents the code to the user.
The user scans the code and registration is complete

##Authentication

The user enters email and password.
The app sends it to Firebase and if everything is correct gets back the user token.
Then uses Token ID to get the encrypted key from the Database.
The user is now asked to enter the verification code from the app.
The loop compares the codes every second and automatically acknowledges when the user gets it right.

##Packages used:

- python-dotenv
- tk
- gcloud
- crypto
- pycryptodome
- pyqrcode
- pyotp
- pyrebase4