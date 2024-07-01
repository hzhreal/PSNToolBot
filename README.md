# PSNToolBot
Discord bot used to mainly add PlayStation 3 avatars to shopping cart, and obtain PlayStation account id from username.

# Tutorial

## NPSSO
For the bot to completely function you need to input your NPSSO 64 character token. This is so you can be authorized to use the PSN API.

How to obtain NPPSO:
- Go to playstation.com and login
- Go to this link https://ca.account.sony.com/api/v1/ssocookie
- Find {"npsso":"<64 character npsso code>"}

## Usage
- Cd into the directory and run pip install -r requirements.txt
- Put your NPSSO and Discord bot token in .env
- Run bot.py

Enjoy!
