#---------------------------
#   Import Libraries
#---------------------------
import clr, codecs, json, os, re, sys, urllib

sys.path.append(os.path.join(os.path.dirname(__file__), "lib")) #point at lib folder for classes / references
clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")

#---------------------------
#   [Required] Script Information
#---------------------------
ScriptName = "Sounds List"
Website = "https://www.twitch.tv/valverdian"
Description = "Make all your sound commands by just adding them to a file."
Creator = "ValVerdian"
Version = "1.0.1"

#---------------------------
#   Define Global Variables
#---------------------------
SettingsFile = os.path.join(os.path.dirname(__file__), "settings.json")

#---------------------------------------
# Classes
#---------------------------------------
class Settings(object):
    def __init__(self, SettingsFile=None):
        if SettingsFile and os.path.isfile(SettingsFile):
            with codecs.open(SettingsFile, encoding="utf-8-sig", mode="r") as f:
                self.__dict__ = json.load(f, encoding="utf-8")
        else:
			self.soundListCommand = "!sounds"
			self.soundsFolderPath = ""
			self.soundListCooldown = 600
			self.soundVolume = 100
			self.perSoundCooldown = 60
			self.perUserSoundCooldown = 120
			self.EnableDebug = False
			self.cost = 100

    def Reload(self, jsondata):
        self.__dict__ = json.loads(jsondata, encoding="utf-8")
        return


#---------------------------
#   [Required] Initialize Data (Only called on load)
#---------------------------
def Init():
	global ScriptSettings
	global Sounds
	ScriptSettings = Settings(SettingsFile)
	Sounds = RetrieveSoundsList(ScriptSettings.soundsFolderPath)
	return

#---------------------------
#   [Required] Execute Data / Process messages
#---------------------------
def Execute(data):

	if not data.IsChatMessage():
		return

	if not (data.GetParam(0)):
		return

	# Now that the command isn't empty we can analyse it
	potentialCommand = data.GetParam(0)

	if ScriptSettings.soundListCommand and potentialCommand.strip() == ScriptSettings.soundListCommand:
		if Parent.IsOnCooldown(ScriptName, ScriptSettings.soundListCommand):
			send_message(ScriptSettings.soundListCommand + " is on cooldown. Time remaining: " + str(Parent.GetCooldownDuration(ScriptName, ScriptSettings.soundListCommand)) + " seconds.")
		else:
			send_message(PrintSounds())
			# Apply Cooldown to !sounds
			Parent.AddCooldown(ScriptName, ScriptSettings.soundListCommand, ScriptSettings.soundListCooldown)

		return
	elif potentialCommand[0] == '!':
		debug_log("trying command: "+ potentialCommand)

		if Parent.IsOnUserCooldown(ScriptName, potentialCommand, data.User):
			send_message(potentialCommand + " is on cooldown. Time remaining: " + str(Parent.GetUserCooldownDuration(ScriptName, potentialCommand, data.User)) + " seconds.")
		elif Parent.IsOnCooldown(ScriptName, potentialCommand):
			send_message(potentialCommand + " is on cooldown. Time remaining: " + str(Parent.GetCooldownDuration(ScriptName, potentialCommand)) + " seconds.")
		else:
			# Get the username from the chat message
			username = Parent.GetDisplayName(data.UserName)
			potentialCommand = potentialCommand.strip().replace('!', '')
			if potentialCommand in Sounds:
				debug_log("Successfully found '" + potentialCommand + "' in Sounds")
				PlaySound(potentialCommand, 100, username)
				#Remove costs
				if Parent.RemovePoints(data.User, username, ScriptSettings.cost):
					debug_log("Removed Points for " + str(data.User) + " " + str(username) + " " + str(ScriptSettings.cost) )
				# Apply both global and user cooldowns
				Parent.AddCooldown(ScriptName, "!"+potentialCommand, ScriptSettings.perSoundCooldown)
				Parent.AddUserCooldown(ScriptName, "!"+potentialCommand, data.User, ScriptSettings.perUserSoundCooldown)
				return

	return

#---------------------------
#   [Required] Update Tick Script
#---------------------------
def Tick():
	return


def send_message(message):
	Parent.SendStreamMessage(message)
	return

def debug_log(message):
	if ScriptSettings.EnableDebug:
		Parent.Log(ScriptName, message)

#---------------------------
#   [Optional] Reload Settings (Called when a user clicks the Save Settings button in the Chatbot UI)
#---------------------------
def ReloadSettings(jsonData):
    return

#---------------------------
#   [Optional] Unload (Called when a user reloads their scripts or closes the bot / cleanup stuff)
#---------------------------
def Unload():
    return

#---------------------------
#   [Optional] ScriptToggled (Notifies you when a user disables your script or enables it)
#---------------------------
def ScriptToggled(state):
    return

def PlaySound(soundName, volume, username): 
	soundPath = ScriptSettings.soundsFolderPath + soundName + ".mp3"
	if os.path.isfile(soundPath):
		Parent.PlaySound(soundPath, ScriptSettings.soundVolume/100)
		send_message("/me " + username + " played sound: '"+ soundName +"'")
		
def RetrieveSoundsList(path):
	if not path:
		return 

	soundFiles = [name for name in os.listdir(path) if name.endswith(".mp3")]

	for i, s in enumerate(soundFiles):
		soundFiles[i] = s.strip().replace('.mp3','')

	debug_log("Sounds loaded: " + str(len(soundFiles)))
	return soundFiles

def PrintSounds():
	listToStr = ' !'.join(map(str, Sounds))
	return listToStr
