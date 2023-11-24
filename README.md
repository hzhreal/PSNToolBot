# PSNToolBot
Discord bot used to mainly add PlayStation 3 avatars to shopping cart, and obtain PlayStation account id from username.

# Requirements
- Latest Python
  ```
  pip install py-cord
  pip install python-dotenv
  pip install
  ```

# Tutorial

## NPSSO
For the bot to completely function you need to input your NPSSO 64 character token. This is so you can be authorized to use the PSN API.

How to obtain NPPSO:
- Go to playstation.com and login
- Go to this link https://ca.account.sony.com/api/v1/ssocookie
- Find {"npsso":"<64 character npsso code>"}
  
if you leave it to "None" the psn.flipscreen.games website will be used to obtain account id. In addition to the avatar functionalities not working.

- Put your NPSSO and Discord token in .env
- Run main.py

Enjoy!
