# Setting up the DnD Discord Server

**At the bottom you can find the command list**

This guide is made up of 3 sections: 

A. [**Server creation**](#server_creation), where it explains how to create the ad hoc server for the Discord bot

B. [**Bot code download**](#bot_download), where it explains how to correctly download the bot code

C. [**Bot setup**](#bot_setup), where it explains how to correctly connect the bot to the Discord server

## A. <a name="server_creation">**Server creation**</a>
1. **Open Discord**: Launch the Discord application on your device.

2. **Enter the link in an internet browser**: Copy the provided template link and paste it into the address bar of any internet browser.
   Template link: **https://discord.new/gwBAdaPzqNcW**

![](/assets/images/Aspose.Words.45baa410-07f8-47dc-b001-d0171d7dcb4f.001.png)

3. **Click on “Continue to Discord”**: After entering the link, you will see an option called “Continue to Discord”. Click on it.

![](/assets/images/Aspose.Words.45baa410-07f8-47dc-b001-d0171d7dcb4f.002.png)

4. **Return to Discord**: Go back to the Discord application. A window should have appeared to create a server based on the provided template.

![](/assets/images/Aspose.Words.45baa410-07f8-47dc-b001-d0171d7dcb4f.003.png)

5. **Enter the desired name**: Enter the name you want for your server in the provided text field.

![](/assets/images/Aspose.Words.45baa410-07f8-47dc-b001-d0171d7dcb4f.004.png)

6. **Click on “Create Server”**: After entering the name, click on the “Create Server” button. Now, you have created your Discord server using the provided template!


## B. <a name="bot_download">**Bot code download**</a>
1. **Open the Repository**: Open your internet browser and navigate to the GitHub repository using the provided link.
   Repository GitHub: <https://github.com/SteveOrDan/DnD-Discord-Bot>      

![](/assets/images/Aspose.Words.45baa410-07f8-47dc-b001-d0171d7dcb4f.005.png)
   
2. **Access the Code**: Once you’re on the repository page, look for a green button labeled “Code” at the top right of the page. Click on this button to open a dropdown menu.    
 
![](/assets/images/Aspose.Words.45baa410-07f8-47dc-b001-d0171d7dcb4f.006.png)
   
3. **Download the ZIP**: In the dropdown menu, you’ll see an option labeled “Download ZIP”. Click on this option to start the download process. The code from the repository will be downloaded as a ZIP file to your computer.

4. **Extract the Files**: After the ZIP file has finished downloading, locate it in your downloads folder or wherever your browser saves downloaded files. Right-click on the ZIP file and select “Extract All” (or a similar option, depending on your operating system). Follow the prompts to extract the files from the ZIP. Once the extraction process is complete, you’ll have a folder containing all the files from the GitHub repository.

## C. <a name="bot_setup">**Bot Setup**</a>
1. **Go to the Discord Developer Portal**: Open your web browser and navigate to the Discord Developer Portal.
2. Discord developer portal: <https://discord.com/developers/applications> and create a new application by clicking on the “New Application” button. Give your application a name and then click “Create”. 

![](/assets/images/Aspose.Words.45baa410-07f8-47dc-b001-d0171d7dcb4f.007.png)

3. **Go to the OAuth2 Page**: In your application’s settings, navigate to the “OAuth2” tab.  

![](/assets/images/Aspose.Words.45baa410-07f8-47dc-b001-d0171d7dcb4f.008.png)

4. **Select Bot under OAuth2 URL Generator**: Under the “OAuth2 URL Generator”, select the “bot” checkbox.

![](/assets/images/Aspose.Words.45baa410-07f8-47dc-b001-d0171d7dcb4f.009.png)

5. **Select Administrator in Bot Permissions**: Scroll down to the “Bot Permissions” section and select the “Administrator” checkbox.

![](/assets/images/Aspose.Words.45baa410-07f8-47dc-b001-d0171d7dcb4f.010.png)

6. **Copy the Generated Link**: At the bottom of the page, you’ll see a generated URL. Click on “Copy” to copy this URL.

![](/assets/images/Aspose.Words.45baa410-07f8-47dc-b001-d0171d7dcb4f.011.png)

7. **Paste the Link in a New Browser Tab**: Open a new tab in your web browser and paste the copied URL into the address bar.

![](/assets/images/Aspose.Words.45baa410-07f8-47dc-b001-d0171d7dcb4f.012.png)

8. **Select Your Server**: A new page will open asking you to select a server. Choose the server where you want to add your bot, then click on the “Authorise” button.  

![](/assets/images/Aspose.Words.45baa410-07f8-47dc-b001-d0171d7dcb4f.013.png)

9. **Navigate to the Bot Tab**: In your application’s settings, find and click on the “Bot” tab. This will take you to the page where your bot’s settings are located.  

![](/assets/images/Aspose.Words.45baa410-07f8-47dc-b001-d0171d7dcb4f.014.png)

10. **Press Reset Token**: On the Bot settings page, find the “Token” section and click on “Reset Token”.

![](/assets/images/Aspose.Words.45baa410-07f8-47dc-b001-d0171d7dcb4f.015.png)
 
11. **Confirm Reset**: A pop-up message will appear asking you to confirm the reset. Click on “Yes, do it!” to confirm.

![](/assets/images/Aspose.Words.45baa410-07f8-47dc-b001-d0171d7dcb4f.016.png)

12. **Enter Password**: You will be asked to enter your password to confirm the reset. Enter your password and proceed.

![](/assets/images/Aspose.Words.45baa410-07f8-47dc-b001-d0171d7dcb4f.017.png)

13. **Copy the New Token**: After resetting, a new token will be generated. Click on “Copy” to copy your bot’s new token. This token is what your bot uses to log in to Discord, so keep it safe!

![](/assets/images/Aspose.Words.45baa410-07f8-47dc-b001-d0171d7dcb4f.018.png)
14. **Locate the Extracted Code Folder**: Navigate to the location on your computer where you previously extracted the bot code. This could be in your “Downloads” folder, “Documents” folder, or wherever you chose to extract the files.

15. **Open the Folder**: Double-click on the folder to open it. You should now see all the files that were contained in the ZIP file.

16. **Open the “constants.py” File**: In the folder, find the file named “constants.py”. Right-click on the file and select “Open with”. Choose your preferred code editor from the list. If you don’t see your code editor, click on “Choose another app” and locate it.

17. **Navigate to the BOT\_TOKEN Line**: Scroll down to the bottom of the “constants.py” file until you find a line that says BOT\_TOKEN. This line should look something like this: 
   BOT\_TOKEN = "MTIxMDIxMzc1NTYxMTM5…".

18. **Replace the Bot Token**: Replace the text between the quotation marks with the bot token you copied in step 13. The line should now look like this: BOT\_TOKEN = " *your\_new\_bot\_token* ".

19. **Save Your Changes**: After replacing the bot token, save your changes. You can usually do this by pressing Ctrl+S or selecting “Save” from the file menu.

20. **Update IDs in the “constants.py” File**: For each entry in the “constants.py” file, you need to find the corresponding element in your Discord server and copy its ID. To do this, right-click on the element (this could be a user, channel, role, etc.) and select “Copy ID”. Then, go back to the “constants.py” file and replace the existing ID with the one you just copied. Make sure to place the new ID in the correct spot in the file.
   Here is how to do it:
      1. **Enable Developer Mode**: First, you need to enable Developer Mode in Discord. To do this, click on the gear icon near your username at the bottom left to open User Settings. Then, navigate to the “Appearance” tab under “App Settings”. Scroll down to the “Advanced” section and toggle on “Developer Mode”.
       2. **Copy Channel ID**: To copy a channel ID, go to the channel from which you want to copy the ID. Right-click on the channel name at the top of the screen and select “Copy ID”. The channel ID is now copied to your clipboard.
       3. **Copy Role ID**: To copy a role ID, you need to go to the server settings. Click on the server name at the top left of the screen and select “Server Settings”. Then, navigate to the “Roles” tab. Here, you’ll see a list of all roles in your server. To copy a role ID, right-click on the role and select “Copy ID”. The role ID is now copied to your clipboard.

## IDs legend:

### General IDs

- GENERAL\_CHAT\_ID: The ID of the general chat channel in your Discord server.
- GUILD\_ID: The ID of your Discord server (also known as a guild in Discord’s API).
- DEFAULT\_ROLES: The default roles that are assigned to new members when they join your server.
- DEFAULT\_CH: The default channel that new members are directed to when they join your server.
- CAMPAIGN\_CHANNELS: The list of channels in your server that are used for campaign discussions.

### Channel IDs

- CAMPAIGN\_CHAT\_ID: The ID of the channel used for campaign chat.
- GET\_FEATURES\_CHAT\_ID: The ID of the channel where users can get features for their characters.
- SET\_ROLES\_CHAT\_ID: The ID of the channel where users can set their roles.
- DM\_CHAT\_ID: The ID of the channel for direct messages.
- RACE\_INFO\_CHAT\_ID: The ID of the channel where information about races is posted.
- CLASS\_INFO\_CHAT\_ID: The ID of the channel where information about classes is posted.
- SET\_RACE\_CHAT\_ID: The ID of the channel where users can set their character’s race.
- SET\_CLASS\_CHAT\_ID: The ID of the channel where users can set their character’s class.

### Player based channels

- PLAYERS\_ROLL\_STATS\_CH\_ID: The ID of the channel where players roll for their character’s stats.
- PLAYERS\_STR\_STAT\_CH\_ID: The ID of the channel where players set their character’s Strength stat.
- PLAYERS\_DEX\_STAT\_CH\_ID: The ID of the channel where players set their character’s Dexterity stat.
- PLAYERS\_CON\_STAT\_CH\_ID: The ID of the channel where players set their character’s Constitution stat.
- PLAYERS\_INT\_STAT\_CH\_ID: The ID of the channel where players set their character’s Intelligence stat.
- PLAYERS\_WIS\_STAT\_CH\_ID: The ID of the channel where players set their character’s Wisdom stat.
- PLAYERS\_CHA\_STAT\_CH\_ID: The ID of the channel where players set their character’s Charisma stat.

### Role IDs

- DM\_ROLE\_ID: The ID of the Dungeon Master role.
- ADVENTURER\_ROLE\_ID: The ID of the Adventurer role.
- CAMPAIGN\_ROLE\_ID: The ID of the Campaign role.
- HUMAN\_ROLE\_ID: The ID of the Human race role.
- STOUT\_ROLE\_ID: The ID of the Stout subrace role.
- LIGHTFOOT\_ROLE\_ID: The ID of the Lightfoot subrace role.
- HALFLING\_ROLE\_ID: The ID of the Halfling race role.
- WOOD\_ELF\_ROLE\_ID: The ID of the Wood Elf subrace role.
- HIGH\_ELF\_ROLE\_ID: The ID of the High Elf subrace role.
- ELF\_ROLE\_ID: The ID of the Elf race role.
- MOUNTAIN\_DWARF\_ROLE\_ID: The ID of the Mountain Dwarf subrace role.
- HILL\_DWARF\_ROLE\_ID: The ID of the Hill Dwarf subrace role.
- DWARF\_ROLE\_ID: The ID of the Dwarf race role.
- WIZARD\_ROLE\_ID: The ID of the Wizard class role.
- ROGUE\_ROLE\_ID: The ID of the Rogue class role.
- FIGHTER\_ROLE\_ID: The ID of the Fighter class role.
- CLERIC\_ROLE\_ID: The ID of the Cleric class role.
- BUILDING\_CHARACTER\_ROLE\_ID: The ID of the role for users who are currently building their character.
- CHOOSING\_ROLE\_ROLE\_ID: The ID of the role for users who are currently choosing their role.

### Player Role IDs

- P1\_ROLE\_ID: The ID of the role for Player 1.
- P2\_ROLE\_ID: The ID of the role for Player 2.
- P3\_ROLE\_ID: The ID of the role for Player 3.
- P4\_ROLE\_ID: The ID of the role for Player 4.
- P5\_ROLE\_ID: The ID of the role for Player 5.

 ### Alignment Role IDs

- LAWFUL\_GOOD\_ROLE\_ID: The ID of the Lawful Good alignment role.
- NEUTRAL\_GOOD\_ROLE\_ID: The ID of the Neutral Good alignment role.
- CHAOTIC\_GOOD\_ROLE\_ID: The ID of the Chaotic Good alignment role.
- LAWFUL\_NEUTRAL\_ROLE\_ID: The ID of the Lawful Neutral alignment role.
- NEUTRAL\_ROLE\_ID: The ID of the Neutral alignment role.
- CHAOTIC\_NEUTRAL\_ROLE\_ID: The ID of the Chaotic Neutral alignment role.
- LAWFUL\_EVIL\_ROLE\_ID: The ID of the Lawful Evil alignment role.
- NEUTRAL\_EVIL\_ROLE\_ID: The ID of the Neutral Evil alignment role.
- CHAOTIC\_EVIL\_ROLE\_ID: The ID of the Chaotic Evil alignment role.

> [!NOTE]
> Here start the command list.

# Commands list

## Campaign management

- **!cc \<user1> \<user2> :** 
  - Channel: #general
  - Context: To start a campaign in the server.
  - Description: Needs at least 3 users but less than 7 users to start a campaign. All users are given the “Choosing role” role, that allows them to select a role in the current campaign (DM or Adventurer). Only 1 DM may exist per campaign.
- **!dc :** 
  - Context: To delete a campaign.
  - Description: This command starts a vote to delete the current campaign. The campaign will be deleted only after every member has typed !dc to confirm the campaign deletion.
- **!sc :** 
  - Context: To start a campaign only when all players has set a role.
  - Description: It’s a command that can be used only after creating a campaign, when all users specified in the !cc command have chosen a role. With this command, the DM is given access to his personal chat #dm-chat. The adventurers instead are given access to a list of channels that allows them to create their character for the campaign.

## Building a character

- **!info :** 
  - Description: Sends a link to download the Basic rules book.
- **!default\_stats :** 
  - Channel: #roll-stats
  - Description: It’s a command that can be used only by Adventurers to avoid randomly rolling for their stats and gives them a preset of stats to assign to their character.
- **!roll\_stats :** 
  - Channel: #roll-stats
  - Description: It’s a command that can be used only by Adventurers in the #roll-stats channel to randomly roll for the 6 stats of a character.
- **!set \<stat_name> :** 
  - Channel: #roll-stats
  - Description: After rolling for the stats, the Adventurer will be asked to assign each number to a stat. This can be done with the !set command.
- **!swap \<stat_1> \<stat_2> :** 
  - Description: If the adventurer made some mistake while assigning the stats, he can use !swap to swap the values of the two specified stats.
- **!set_alignment \<alignment> :**
  - Channel: #character-features
  - Description: Sets the alignment for the user’s character.
- **!complete_char :** 
  - Context: After completing the character creation.
  - Description: The command checks if the player has set a class, a race, an alignment and all 6 stats. If everything is set, the bot sends a message with all the information of the character created.
- **!quick_char_create \<class> \<race> \<STR_value> \<DEX_value> \<CON_value> \<INT_value> \<WIS_value> \<CHA_value> \<alignment_if_not_N> :**
  - Context: After using !sc, only for an adventurer.
  - Description: Allows an adventurer to quickly create a character if they already know how to create one. Every player is given 27 points, and they can “spend” those points in stats. Each stat value has a corresponding value in points used, and the player cannot exceed that limit, otherwise the character creation will be aborted.

## Optional character features

- **!set_name \<character_name>:**
  - Channel: #character-features
  - Context: While creating a character (Optional)
  - Description: Changes the nickname of the user in the server to the specified nickname.
- **!random_name \<race> \<gender> \<clan_if_human>:**
  - Description: Generates a random name based on the given parameters. The name is sent by the bot in the same chat where the messages is written.
- **!set_bg \<background>:**
  - Channel: #character-features
  - Context: While creating a character (Optional)
  - Description: Sets the background for the user’s character.
- **!set_traits \<traits >:**
  - Channel: #character-features
  - Context: While creating a character (Optional)
  - Description: Sets the traits for the user’s character.
- **!set_ideals \<ideals>:**
  - Channel: #character-features
  - Context: While creating a character (Optional)
  - Description: Sets the ideals for the user’s character.
- **!set_bonds \<bonds >:**
  - Channel: #character-features
  - Context: While creating a character (Optional)
  - Description: Sets the bonds for the user’s character.
- **!set_flaws \<flaws >:**
  - Channel: #character-features
  - Context: While creating a character (Optional)
  - Description: Sets the flaws for the user’s character.

## Transactions and items

- **!request_buy \<item_name> \<amount = 1>:**
  - Channel: None (Usually#campaign-chat)
  - Context: After completing a character.
  - Description: An adventurer can send the DM a request to buy an item from the data base. By default, the amount is set to 1, but the adventurer can specify a different number. The DM will receive a notification in #dm-chat with all the information of the transaction. The transaction can only be started if the adventurer has enough space in the inventory.
- **!set_buy_price \<user> \<item> \<price> \<currency>:**
  - Channel: None (Usually in #dm-chat)
  - Context: When receiving a request to buy an item from an adventurer.
  - Description: The DM must specify the user and the item of the transaction which he want to set a price for. The price can be expressed with a number followed by the type of currency (CP, GP …), this way the DM will change the default price of the transaction. If he thinks that the default price is good enough, he can type “default” instead of the price. After setting the price the adventurer will receive a notification with the price set by the DM.
- **!accept_buy \<item> :**
  - Channel: None (Usually #campaign-chat)
  - Context: After the DM has set a price for a transaction previously requested.
  - Description: The adventurer accepts the offer of the DM, buys the item(s) by adding them to the inventory and closes the transaction.
- **!refuse_buy \<item> :** 
  - Channel: None (Usually #campaign-chat)
  - Context: After the DM has set a price for a transaction previously requested.
  - Description: The adventurer refuses the offer of the DM and deletes the transaction.
- **An adventurer can also buy items from his inventory.** 
  - The logic and the commands are quite the same as the one for buying, with the only difference that the commands need “**sell**” instead of “**buy**”.
- **!get_all_transactions :**
  - Context: Only for the DM to check which transactions are still ongoing.
  - Description: The bot sends a message with all the ongoing transactions.
- **!get_purse \<member> :**
  - Channel: None (Usually #campaign-chat)
  - Context: After creating the character.
  - Description: The bot sends a message showing all the coins of a character divided by currency type.
- **!equip \<item> :**
  - Context: During adventure.
  - Description: A character can decide to equip an item (armor or weapon) and if the item is in the inventory the current equipped item will be swapped with the new one. The old one will be put in the inventory. Equipping an armor too heavy for the character, will cause him to lose some speed.
- **!unequip \<item_type> :**
  - Context: During adventure.
  - Description: A character can decide to unequip an item (“armor” or “weapon”) and if the item is equipped, it is moved back to the inventory.

## Dice rolls

- **!ability_check \<ability> :**
  - Context: Whenever the DM request an ability check.
  - Description: The user rolls a D20 and adds the modifier of the checked stat. 1 is a critical failure, while 20 is a critical hit.
- **!roll_dice \<dice> :**
  - Description: Just rolls the dice specified in the command (1d6, 1d20 …)
- **!saving_throw \<ability> :**
  - Context: Whenever requested by the DM.
  - Description: The user throws a D20 and adds the stat modifier and the proficiency bonus (if available)

## Combat

- **!create_monster \<name> \<AC> \<HP> \<STR> \<DEX> \<CON> \<INT> \<WIS> \<CHA> \<attack_bonus> \<dice_num> \<damage_dice> \<damage_bonus>:**
  - Description: Only for the DM. Allows him to create a new monster and add it to the monster data base. After creating the monster, it can be used in an encounter for the adventurers.
- **!set_encounter \<monster_name_1>:\<count>, \<monster_name_2>:\<count>, ... :**
  - Description: Creates an encounter for the adventurers to clear.
- **!attack_monster \<ability> \<monster_id> :**
  - Context: After the DM has created an encounter.
  - Description: The adventurer can decide with which stat he wants to attack a certain monster. Monster IDs are sent by the bot after the encounter has been set by the DM. 
- **!attack_player \<member> \<monster> :**
  - Context: During a fight.
  - Description: Only for the DM. Allows a monster to attack an adventurer and eventually deal damage to him.

## Spells

- **!prepare \<spell_name> :**
  - Description: Allows a cleric or a wizard to prepare a spell that can be casted. The adventurer needs to know the spell he is preparing.
- **!unprepare \<spell_name> :**
  - Description: Allows a wizard or a cleric to remove a spell from the list of prepared spells.
- **!cast \<spell_name> \<parameters> :** 
  - Description: This command is a bit particular, since its parameters may change depending on the spell that the adventurer wants to cast.
  - Light: \<object>
    - Cast light on the specified object.
  - Resistance: \<user>
    - Cast resistance on a user and they can add a d4 to a saving roll of their choice.
  - Mage hand
  - Spare the dying: \<target>
    - Cast spare the dying on the specified target.
  - Detect magic
  - Healing word: \<user>
    - Heals the specified user by d4 + WIS mod.
  - Prestidigitation: \<effect>
    - Cast prestidigitation with the effect specified by the effect parameter.
  - Magic missile: \<target1>, \<target2>, \<target3>
    - Cast magic missile 3 targets and damages them. To use this spell the casted needs to be involved in an encounter, and the target must be monsters from that same encounter. 
- **!rest :**
  - Description: The adventurer can rest and restore all available slots to cast magic spells.

## Miscellaneous

- **!get_prepared_spells :**
  - Description: The bot sends a message with all the user’s prepared spells.
- **!get_known_spells :**
  - Description: The bot sends a message with all the user’s known spells.
- **!get_inventory :** 
  - The bot sends a message with al the items in the user’s inventory.
- **!get_equipment :** 
  - The bot sends a message with the user’s current equipped weapon and armor.
- **!get_member_info \<member> :**
  - Description: The bot sends a message with all the information available of the specified user.
- **!get_all_monsters :** 
  - Description: The bot sends a message containing all the monsters stored in the database and their information.
