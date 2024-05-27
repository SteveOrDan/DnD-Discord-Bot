**Commands list**

**Campaign management**

- **!cc <user1> <user2> …** **:** 
  - Channel: #general
  - Context: To start a campaign in the server.
  - Description: Needs at least 3 users but less than 7 users to start a campaign. All users are given the “Choosing role” role, that allows them to select a role in the current campaign (DM or Adventurer). Only 1 DM may exist per campaign.
- **!dc** **:** 
  - Context: To delete a campaign.
  - Description: This command starts a vote to delete the current campaign. The campaign will be deleted only after every member has typed !dc to confirm the campaign deletion.
- **!sc** **:** 
  - Context: To start a campaign only when all players has set a role.
  - Description: It’s a command that can be used only after creating a campaign, when all users specified in the !cc command have chosen a role. With this command, the DM is given access to his personal chat #dm-chat. The adventurers instead are given access to a list of channels that allows them to create their character for the campaign.

**Building a character**

- **!info** **:** 
  - Description: Sends a link to download the Basic rules book.
- **!default\_stats** **:** 
  - Channel: #roll-stats
  - Description: It’s a command that can be used only by Adventurers to avoid randomly rolling for their stats and gives them a preset of stats to assign to their character.
- **!roll\_stats** **:** 
  - Channel: #roll-stats
  - Description: It’s a command that can be used only by Adventurers in the #roll-stats channel to randomly roll for the 6 stats of a character.
- **!set <stat\_name>** **:** 
  - Channel: #roll-stats
  - Description: After rolling for the stats, the Adventurer will be asked to assign each number to a stat. This can be done with the !set command.
- **!swap <stat\_1> <stat\_2> :** 
  - Description: If the adventurer made some mistake while assigning the stats, he can use !swap to swap the values of the two specified stats.
- **!set\_alignment <alignment> :**
  - Channel: #character-features
  - Description: Sets the alignment for the user’s character.
- **!complete\_char :** 
  - Context: After completing the character creation.
  - Description: The command checks if the player has set a class, a race, an alignment and all 6 stats. If everything is set, the bot sends a message with all the information of the character created.
- **!quick\_char\_create <class> <race> <STR\_value> <DEX\_value> <CON\_value> <INT\_value> <WIS\_value> <CHA-value> <alignment\_if\_not\_N> :**
  - Context: After using !sc, only for an adventurer.
  - Description: Allows an adventurer to quickly create a character if they already know how to create one. Every player is given 27 points, and they can “spend” those points in stats. Each stat value has a corresponding value in points used, and the player cannot exceed that limit, otherwise the character creation will be aborted.

**Optional character features**

- **!set\_name <character\_name>:**
  - Channel: #character-features
  - Context: While creating a character (Optional)
  - Description: Changes the nickname of the user in the server to the specified nickname.
- **!random\_name <race> <gender> <clan\_if\_human>:**
  - Description: Generates a random name based on the given parameters. The name is sent by the bot in the same chat where the messages is written.
- **!set\_bg <background>:**
  - Channel: #character-features
  - Context: While creating a character (Optional)
  - Description: Sets the background for the user’s character.
- **!set\_traits <traits >:**
  - Channel: #character-features
  - Context: While creating a character (Optional)
  - Description: Sets the traits for the user’s character.
- **!set\_ideals <ideals>:**
  - Channel: #character-features
  - Context: While creating a character (Optional)
  - Description: Sets the ideals for the user’s character.
- **!set\_bonds <bonds >:**
  - Channel: #character-features
  - Context: While creating a character (Optional)
  - Description: Sets the bonds for the user’s character.
- **!set\_flaws <flaws >:**
  - Channel: #character-features
  - Context: While creating a character (Optional)
  - Description: Sets the flaws for the user’s character.

**Transactions and items**

- **!request\_buy <item\_name> <amount = 1>:**
  - Channel: None (Usually#campaign-chat)
  - Context: After completing a character.
  - Description: An adventurer can send the DM a request to buy an item from the data base. By default, the amount is set to 1, but the adventurer can specify a different number. The DM will receive a notification in #dm-chat with all the information of the transaction. The transaction can only be started if the adventurer has enough space in the inventory.
- **!set\_buy\_price <user> <item> <price> <currency>:**
  - Channel: None (Usually in #dm-chat)
  - Context: When receiving a request to buy an item from an adventurer.
  - Description: The DM must specify the user and the item of the transaction which he want to set a price for. The price can be expressed with a number followed by the type of currency (CP, GP …), this way the DM will change the default price of the transaction. If he thinks that the default price is good enough, he can type “default” instead of the price. After setting the price the adventurer will receive a notification with the price set by the DM.
- **!accept\_buy <item> :**
  - Channel: None (Usually #campaign-chat)
  - Context: After the DM has set a price for a transaction previously requested.
  - Description: The adventurer accepts the offer of the DM, buys the item(s) by adding them to the inventory and closes the transaction.
- **!refuse\_buy <item> :** 
  - Channel: None (Usually #campaign-chat)
  - Context: After the DM has set a price for a transaction previously requested.
  - Description: The adventurer refuses the offer of the DM and deletes the transaction.
- **An adventurer can also buy items from his inventory.** 
  - The logic and the commands are quite the same as the one for buying, with the only difference that the commands need “**sell**” instead of “**buy**”.
- **!get\_all\_transactions :**
  - Context: Only for the DM to check which transactions are still ongoing.
  - Description: The bot sends a message with all the ongoing transactions.
- **!get\_purse <member> :**
  - Channel: None (Usually #campaign-chat)
  - Context: After creating the character.
  - Description: The bot sends a message showing all the coins of a character divided by currency type.
- **!equip <item> :**
  - Context: During adventure.
  - Description: A character can decide to equip an item (armor or weapon) and if the item is in the inventory the current equipped item will be swapped with the new one. The old one will be put in the inventory. Equipping an armor too heavy for the character, will cause him to lose some speed.
- **!unequip <item\_type> :**
  - Context: During adventure.
  - Description: A character can decide to unequip an item (“armor” or “weapon”) and if the item is equipped, it is moved back to the inventory.

**Dice rolls**

- **!ability\_check <ability> :**
  - Context: Whenever the DM request an ability check.
  - Description: The user rolls a D20 and adds the modifier of the checked stat. 1 is a critical failure, while 20 is a critical hit.
- **!roll\_dice <dice> :**
  - Description: Just rolls the dice specified in the command (1d6, 1d20 …)
- **!saving\_throw <ability> :**
  - Context: Whenever requested by the DM.
  - Description: The user throws a D20 and adds the stat modifier and the proficiency bonus (if available)

**Combat**

- **!create\_monster <name> <AC> <HP> <STR> <DEX> <CON> <INT> <WIS> <CHA> <attack\_bonus> <dice\_num> <damage\_dice> <damage\_bonus>:**
  - Description: Only for the DM. Allows him to create a new monster and add it to the monster data base. After creating the monster, it can be used in an encounter for the adventurers.
- **!set\_encounter <monster\_name\_1>:<count>, <monster\_name\_2>:<count>, ... :**
  - Description: Creates an encounter for the adventurers to clear.
- **!attack\_monster <ability> <monster\_id> :**
  - Context: After the DM has created an encounter.
  - Description: The adventurer can decide with which stat he wants to attack a certain monster. Monster IDs are sent by the bot after the encounter has been set by the DM. 
- **!attack\_player <member> <monster> :**
  - Context: During a fight.
  - Description: Only for the DM. Allows a monster to attack an adventurer and eventually deal damage to him.

**Spells**

- **!prepare <spell\_name> :**
  - Description: Allows a cleric or a wizard to prepare a spell that can be casted. The adventurer needs to know the spell he is preparing.
- **!unprepare <spell\_name> :**
  - Description: Allows a wizard or a cleric to remove a spell from the list of prepared spells.
- **!cast <spell\_name> <parameters> :** 
  - Description: This command is a bit particular, since its parameters may change depending on the spell that the adventurer wants to cast.
  - Light: <object>
    - Cast light on the specified object.
  - Resistance: <user>
    - Cast resistance on a user and they can add a d4 to a saving roll of their choice.
  - Mage hand
  - Spare the dying: <target>
    - Cast spare the dying on the specified target.
  - Detect magic
  - Healing word: <user>
    - Heals the specified user by d4 + WIS mod.
  - Prestidigitation: <effect>
    - Cast prestidigitation with the effect specified by the effect parameter.
  - Magic missile: <target1>, <target2>, <target3>
    - Cast magic missile 3 targets and damages them. To use this spell the casted needs to be involved in an encounter, and the target must be monsters from that same encounter. 
- **!rest :**
  - Description: The adventurer can rest and restore all available slots to cast magic spells.

**Miscellaneous**

- **!get\_prepared\_spells :**
  - Description: The bot sends a message with all the user’s prepared spells.
- **!get\_known\_spells :**
  - Description: The bot sends a message with all the user’s known spells.
- **!get\_inventory :** 
  - The bot sends a message with al the items in the user’s inventory.
- **!get\_equipment :** 
  - The bot sends a message with the user’s current equipped weapon and armor.
- **!get\_member\_info <member> :**
  - Description: The bot sends a message with all the information available of the specified user.
- **!get\_all\_monsters :** 
  - Description: The bot sends a message containing all the monsters stored in the database and their information.

