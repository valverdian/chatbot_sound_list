# Sounds List
This [Streamlabs Chatbot](https://streamlabs.com/chatbot) script is an easy way to add all / remove sound commands to your bot.
Load up your chatbot, pass in a path, refresh your scripts, Set everything else and then the script will take care of playing all of those sounds as commands. 

This is intended to be used with **Streamlabs Chatbot** only and has been built primarly for use with Twitch. 


## Getting Started 
- Start with setting up your chatbot to accept and run scripts. You can follow this [guide](https://streamlabs.com/content-hub/post/chatbot-scripts-desktop). 
- Fill a folder with .mp3 files, name each file as the command you want it to be. 
- Startup the chatbot and navigate to the scripts tab on the bottom left (you need to be signed in to see this).
- Click the import button and add the .zip file from the latest version to import it.
- Most of the fields should be set with reasonable defaults, so you only need to set the path to your folder full of .mp3 files. 

**Example path**: ```G:\chatbot_sounds\mp3\```

```
note: (the \ at the end is very important)
```

- Save and enable the script then click the `reload scripts` button to load in your sound commands.
- Try it out on the chat. You should be able to get a list of sound commands by typing in the sound list command (!sounds by default) and any of those sounds should work and respond to the cooldowns provided.

## Additional Info
- All sound commands will be the name with a ! at the start. For example a sound named:
"shouting" will become a command "!shouting". 
- After adding / changing the sounds path, the sounds list will not update until you refresh your scripts. 
- if you leave the **Sound List Command** field empty. It disables the list command.

## Thank you
I hope this script is useful for you. If you have any thoughts on it, raise a github issue with a suggestion or lemme know while I'm [streaming](https://www.twitch.tv/valverdian) or send me an @ on [twitter](https://www.twitter.com/valverdian)!
