# Unfair-Fest-Bot
A unfair bot for the mobile game Bike Race that plays tournaments for you and wins them.

### Options
Inside ```unfair_fest_bot/config/config.json``` you got some options you can change:

```json
"player": {
	"fest_id": "your_fest_player_account_id",
	"token": "your_fest_account_token"
},
```
The above is the setting for your account, you can get these by intercepting a http request from the game.
Also a nice thing, the token never expires so once you have your token you can just keep using it!

Then we also got bot configurations:
```json
"bot_configurations": {
	"auto_claim_tourneys": true,
	"auto_evolve": true,
	"spare_turbo_bikes": true,
	"play_before_end_in_seconds": 180
}
```
As of now, there's a limit of options and I'm not sure if I will create more.
However, you can create options yourself & if you feel like it make a PR on it!

So let me explain what the options are for:
- ```auto_claim_tourneys```: If you have open tourney rewards, and you want the bot to claim them for you, you set this to true, if not you have to claim them yourself and can possibly run out of storage space if you don't do this regulary.
- ```auto_evolve```: If the bot claims rewards for you, and you have this option on, it will evolve the highest star bike for you with the reward item. 
    - NOTE: This will not evolve the reward item if you don't have the bike in your garage yet!
- ```spare_turbo_bikes```: If you have auto_evolve on, it will evolve reward items even if it's a Turbo part, which I defenitly didn't like so I made this option. If you return this to true, it will never evolve turbo bike rewards!
- ```play_before_end_in_seconds```: When does the bot play the tournaments? If you set this too a high value, it will play them instantly after you join which can result in you setting times when no one else has yet & you may loose because you ran out of attempts. If you set it too low, you may end up not being able to set times before the tourneys ends. I figured 180 seconds works like a charm for me but you might want to play around with this a little.

### How to run it?
In main,py, I have a very ugly statement:
```python
    # Best way of doing this? No, probably not.
    while True:
        FestBot(fest_player).play_all_tourneys()
```

Meaning you can run ```python main.py``` or ```python3 main.py``` if ```python``` runs python 2 for you.
You also need the requests libary installed (```pip install requests```)

The best way to run this, is using some hosting option like PythonAnywhere where you can run a always on task.
This is nice, because if the script for some reason failed to stay running, it will just restart which I think is great.
On PythonAnywhere you just need a $5 account in order to do this.