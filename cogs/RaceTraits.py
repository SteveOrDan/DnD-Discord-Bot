import discord
import costants

from discord.ext import commands


class RaceTraits(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role("Campaign")
    async def dwarf(self, ctx):
        if ctx.channel.id == costants.RACE_INFO_CHAT_ID:
            await ctx.send(embed=embed_dwarf)

    @commands.command()
    @commands.has_role("Campaign")
    async def mountain_dwarf(self, ctx):
        if ctx.channel.id == costants.RACE_INFO_CHAT_ID:
            await ctx.send(embed=embed_mountain_dwarf)

    @commands.command()
    @commands.has_role("Campaign")
    async def hill_dwarf(self, ctx):
        if ctx.channel.id == costants.RACE_INFO_CHAT_ID:
            await ctx.send(embed=embed_hill_dwarf)

    @commands.command()
    @commands.has_role("Campaign")
    async def elf(self, ctx):
        if ctx.channel.id == costants.RACE_INFO_CHAT_ID:
            await ctx.send(embed=embed_elf)

    @commands.command()
    @commands.has_role("Campaign")
    async def high_elf(self, ctx):
        if ctx.channel.id == costants.RACE_INFO_CHAT_ID:
            await ctx.send(embed=embed_high_elf)

    @commands.command()
    @commands.has_role("Campaign")
    async def wood_elf(self, ctx):
        if ctx.channel.id == costants.RACE_INFO_CHAT_ID:
            await ctx.send(embed=embed_wood_elf)

    @commands.command()
    @commands.has_role("Campaign")
    async def halfling(self, ctx):
        if ctx.channel.id == costants.RACE_INFO_CHAT_ID:
            await ctx.send(embed=embed_halfling)

    @commands.command()
    @commands.has_role("Campaign")
    async def stout(self, ctx):
        if ctx.channel.id == costants.RACE_INFO_CHAT_ID:
            await ctx.send(embed=embed_stout)

    @commands.command()
    @commands.has_role("Campaign")
    async def light_foot(self, ctx):
        if ctx.channel.id == costants.RACE_INFO_CHAT_ID:
            await ctx.send(embed=embed_lightfoot)

    @commands.command()
    @commands.has_role("Campaign")
    async def human(self, ctx):
        if ctx.channel.id == costants.RACE_INFO_CHAT_ID:
            await ctx.send(embed=embed_human)


async def setup(bot):
    await bot.add_cog(RaceTraits(bot))


# Dwarf
embed_dwarf = discord.Embed(title="Dwarf Traits",
                            description="Your dwarf character has an assortment of inborn abilities, part and parcel of dwarven nature.",
                            colour=0x6e1a01)
embed_dwarf.add_field(name="Ability score increase",
                      value="Your Constitution score increases by 2.",
                      inline=False)
embed_dwarf.add_field(name="Age",
                      value="Dwarves mature at the same rate as humans, but they’re considered young until they reach the age of 50. On average, they live about 350 years.",
                      inline=False)
embed_dwarf.add_field(name="Alignment",
                      value="Most dwarves are lawful, believing firmly in the benefits of a well-ordered society. They tend toward good as well, with a strong sense of fair play and a belief that everyone deserves to share in the benefits of a just order.",
                      inline=False)
embed_dwarf.add_field(name="Size",
                      value="Dwarves stand between 4 and 5 feet tall and average about 150 pounds. Your size is Medium.",
                      inline=False)
embed_dwarf.add_field(name="Speed",
                      value="Your base walking speed is 25 feet. Your speed is not reduced by wearing heavy armor.",
                      inline=False)
embed_dwarf.add_field(name="Darkvision",
                      value="Accustomed to life underground, you have superior vision in dark and dim conditions. You can see in dim light within 60 feet of you as if it were bright light, and in darkness as if it were dim light. You can’t discern color in darkness, only shades of gray.",
                      inline=False)
embed_dwarf.add_field(name="Dwarven Resilience",
                      value="You have advantage on saving throws against poison, and you have resistance against poison damage (explained in chapter 9).",
                      inline=False)
embed_dwarf.add_field(name="Dwarven Combat Training",
                      value="You have proficiency with the battleaxe, handaxe, light hammer, and warhammer.",
                      inline=False)
embed_dwarf.add_field(name="Tool Proficiency",
                      value="You gain proficiency with the artisan’s tools of your choice: smith’s tools, brewer’s supplies, or mason’s tools.",
                      inline=False)
embed_dwarf.add_field(name="Stonecunning",
                      value="Whenever you make an Intelligence (History) check related to the origin of stonework, you are considered proficient in the History skill and add double your proficiency bonus to the check, instead of your normal proficiency bonus.",
                      inline=False)
embed_dwarf.add_field(name="Languages",
                      value="You can speak, read, and write Common and Dwarvish. Dwarvish is full of hard consonants and guttural sounds, and those characteristics spill over into whatever other language a dwarf might speak.",
                      inline=False)
embed_dwarf.add_field(name="Subrace",
                      value="Two main subraces of dwarves populate the worlds of D&D: hill dwarves and mountain dwarves.",
                      inline=False)

embed_hill_dwarf = discord.Embed(title="Hill Dwarf Traits",
                                 description="As a hill dwarf, you have keen senses, deep intuition, and remarkable resilience. The gold dwarves of Faerûn in their mighty southern kingdom are hill dwarves, as are the exiled Neidar and the debased Klar of Krynn in the Dragonlance setting.",
                                 colour=0x6e1a01)
embed_hill_dwarf.add_field(name="Ability score increase",
                           value="Your Wisdom score increases by 1.",
                           inline=False)
embed_hill_dwarf.add_field(name="Dwarven Toughness",
                           value="Your hit point maximum increases by 1, and it increases by 1 every time you gain a level.",
                           inline=False)

embed_mountain_dwarf = discord.Embed(title="Mountain Dwarf Traits",
                                     description="As a mountain dwarf, you’re strong and hardy, accustomed to a difficult life in rugged terrain. You’re probably on the tall side (for a dwarf), and tend toward lighter coloration. The shield dwarves of northern Faerûn, as well as the ruling Hylar clan and the noble Daewar clan of Dragonlance, are mountain dwarves.",
                                     colour=0x6e1a01)
embed_mountain_dwarf.add_field(name="Ability score increase",
                               value="Your Strength score increases by 2.",
                               inline=False)
embed_mountain_dwarf.add_field(name="Dwarven Armor Training",
                               value="You have proficiency with light and medium armor.",
                               inline=False)

# Elf
embed_elf = discord.Embed(title="Elf Traits",
                          description="Your elf character has a variety of natural abilities, the result of thousands of years of elven refinement.",
                          colour=0x0ac91d)
embed_elf.add_field(name="Ability score increase",
                    value="Your Dexterity score increases by 2.",
                    inline=False)
embed_elf.add_field(name="Age",
                    value="Although elves reach physical maturity at about the same age as humans, the elven understanding of adulthood goes beyond physical growth to encompass worldly experience. An elf typically claims adulthood and an adult name around the age of 100 and can live to be 750 years old.",
                    inline=False)
embed_elf.add_field(name="Alignment",
                    value="Elves love freedom, variety, and self-expression, so they lean strongly toward the gentler aspects of chaos. They value and protect others’ freedom as well as their own, and they are more often good than not.",
                    inline=False)
embed_elf.add_field(name="Size",
                    value="Elves range from under 5 to over 6 feet tall and have slender builds. Your size is Medium.",
                    inline=False)
embed_elf.add_field(name="Speed",
                    value="Your base walking speed is 30 feet.",
                    inline=False)
embed_elf.add_field(name="Darkvision",
                    value="Accustomed to twilit forests and the night sky, you have superior vision in dark and dim conditions. You can see in dim light within 60 feet of you as if it were bright light, and in darkness as if it were dim light. You can’t discern color in darkness, only shades of gray. ",
                    inline=False)
embed_elf.add_field(name="Keen Senses",
                    value="have proficiency in the Perception skill.",
                    inline=False)
embed_elf.add_field(name="Fey Ancestry",
                    value="You have advantage on saving throws against being charmed, and magic can’t put you to sleep.",
                    inline=False)
embed_elf.add_field(name="Trance",
                    value="Elves don’t need to sleep. Instead, they meditate deeply, remaining semiconscious, for 4 hours a day. (The Common word for such meditation is “trance.”) While meditating, you can dream after a fashion; such dreams are actually mental exercises that have become reflexive through years of practice. After resting in this way, you gain the same benefit that a human does from 8 hours of sleep.",
                    inline=False)
embed_elf.add_field(name="Languages",
                    value="You can speak, read, and write Common and Elvish. Elvish is fluid, with subtle intonations and intricate grammar. Elven literature is rich and varied, and their songs and poems are famous among other races. Many bards learn their language so they can add Elvish ballads to their repertoires.",
                    inline=False)
embed_elf.add_field(name="Subrace",
                    value="Ancient divides among the elven people resulted in three main subraces: high elves, wood elves, and dark elves, who are commonly called drow. This document presents two of these subraces to choose from. In some worlds, these subraces are divided still further (such as the sun elves and moon elves of the Forgotten Realms), so if you wish, you can choose a narrower subrace.",
                    inline=False)

embed_high_elf = discord.Embed(title="High Elf Traits",
                               description="As a high elf, you have a keen mind and a mastery of at least the basics of magic. In many of the worlds of D&D, there are two kinds of high elves. One type (which includes the gray elves and valley elves of Greyhawk, the Silvanesti of Dragonlance, and the sun elves of the Forgotten Realms) is haughty and reclusive, believing themselves to be superior to non-elves and even other elves. The other type (including the high elves of Greyhawk, the Qualinesti of Dragonlance, and the moon elves of the Forgotten Realms) are more common and more friendly, and often encountered among humans and other races. The sun elves of Faerûn (also called gold elves or sunrise elves) have bronze skin and hair of copper, black, or golden blond. Their eyes are golden, silver, or black. Moon elves (also called silver elves or gray elves) are much paler, with alabaster skin sometimes tinged with blue. They often have hair of silver-white, black, or blue, but various shades of blond, brown, and red are not uncommon. Their eyes are blue or green and flecked with gold.",
                               colour=0x0ac91d)
embed_high_elf.add_field(name="Ability score increase",
                         value="Your Intelligence score increases by 1.",
                         inline=False)
embed_high_elf.add_field(name="Elf Weapon Training",
                         value="You have proficiency with the longsword, shortsword, shortbow, and longbow.",
                         inline=False)
embed_high_elf.add_field(name="Cantrip",
                         value="You know one cantrip of your choice from the wizard spell list. Intelligence is your spellcasting ability for it.",
                         inline=False)
embed_high_elf.add_field(name="Extra Language",
                         value="You can speak, read, and write one extra language of your choice.",
                         inline=False)

embed_wood_elf = discord.Embed(title="Wood Elf Traits",
                               description="As a wood elf, you have keen senses and intuition, and your fleet feet carry you quickly and stealthily through your native forests. This category includes the wild elves (grugach) of Greyhawk and the Kagonesti of Dragonlance, as well as the races called wood elves in Greyhawk and the Forgotten Realms. In Faerûn, wood elves (also called wild elves, green elves, or forest elves) are reclusive and distrusting of non-elves. Wood elves’ skin tends to be copperish in hue, sometimes with traces of green. Their hair tends toward browns and blacks, but it is occasionally blond or copper-colored. Their eyes are green, brown, or hazel.",
                               colour=0x0ac91d)
embed_wood_elf.add_field(name="Ability score increase",
                         value="Your Wisdom score increases by 1.",
                         inline=False)
embed_wood_elf.add_field(name="Elf Weapon Training",
                         value="YYou have proficiency with the longsword, shortsword, shortbow, and longbow.",
                         inline=False)
embed_wood_elf.add_field(name="Fleet of Foot",
                         value="Your base walking speed increases to 35 feet.",
                         inline=False)
embed_wood_elf.add_field(name="Mask of the Wild",
                         value="You can attempt to hide even when you are only lightly obscured by foliage, heavy rain, falling snow, mist, and other natural phenomena.",
                         inline=False)

# Halfling
embed_halfling = discord.Embed(title="Halfling Traits",
                               description="Your halfling character has a number of traits in common with all other halflings.",
                               colour=0x969696)
embed_halfling.add_field(name="Ability score increase",
                         value="Your Dexterity score increases by 2.",
                         inline=False)
embed_halfling.add_field(name="Age",
                         value="A halfling reaches adulthood at the age of 20 and generally lives into the middle of his or her second century.",
                         inline=False)
embed_halfling.add_field(name="Alignment",
                         value="Most halflings are lawful good. As a rule, they are good-hearted and kind, hate to see others in pain, and have no tolerance for oppression. They are also very orderly and traditional, leaning heavily on the support of their community and the comfort of their old ways.",
                         inline=False)
embed_halfling.add_field(name="Size",
                         value="Halflings average about 3 feet tall and weigh about 40 pounds. Your size is Small.",
                         inline=False)
embed_halfling.add_field(name="Speed",
                         value="Your base walking speed is 25 feet.",
                         inline=False)
embed_halfling.add_field(name="Lucky",
                         value="When you roll a 1 on the d20 for an attack roll, ability check, or saving throw, you can reroll the die and must use the new roll.",
                         inline=False)
embed_halfling.add_field(name="Brave",
                         value="You have advantage on saving throws against being frightened.",
                         inline=False)
embed_halfling.add_field(name="Halfling Nimbleness",
                         value="You can move through the space of any creature that is of a size larger than yours.",
                         inline=False)
embed_halfling.add_field(name="Languages",
                         value="You can speak, read, and write Common and Halfling. The Halfling language isn’t secret, but halflings are loath to share it with others. They write very little, so they don’t have a rich body of literature. Their oral tradition, however, is very strong. Almost all halflings speak Common to converse with the people in whose lands they dwell or through which they are traveling.",
                         inline=False)
embed_halfling.add_field(name="Subrace",
                         value="The two main kinds of halfling, lightfoot and stout, are more like closely related families than true subraces.",
                         inline=False)

embed_lightfoot = discord.Embed(title="Lightfoot Trails",
                                description="As a lightfoot halfling, you can easily hide from notice, even using other people as cover. You’re inclined to be affable and get along well with others. In the Forgotten Realms, lightfoot halflings have spread the farthest and thus are the most common variety. Lightfoots are more prone to wanderlust than other halflings, and often dwell alongside other races or take up a nomadic life. In the world of Greyhawk, these halflings are called hairfeet or tallfellows.",
                                colour=0x969696)
embed_lightfoot.add_field(name="Ability score increase",
                          value="Your Charisma score increases by 1.",
                          inline=False)
embed_lightfoot.add_field(name="Naturally Stealthy",
                          value="You can attempt to hide even when you are obscured only by a creature that is at least one size larger than you.",
                          inline=False)

embed_stout = discord.Embed(title="Stout Trails",
                            description="As a stout halfling, you’re hardier than average and have some resistance to poison. Some say that stouts have dwarven blood. In the Forgotten Realms, these halflings are called stronghearts, and they’re most common in the south.",
                            colour=0x969696)
embed_stout.add_field(name="Ability score increase",
                      value="Your Constitution score increases by 1.",
                      inline=False)
embed_stout.add_field(name="Stout Resilience",
                      value="You have advantage on saving throws against poison, and you have resistance against poison damage.",
                      inline=False)

# Human
embed_human = discord.Embed(title="Human Traits",
                            description="It’s hard to make generalizations about humans, but your human character has these traits.",
                            colour=0x1791fc)
embed_human.add_field(name="Ability score increase",
                      value="Your ability scores each increase by 1.",
                      inline=False)
embed_human.add_field(name="Age",
                      value="Humans reach adulthood in their late teens and live less than a century.",
                      inline=False)
embed_human.add_field(name="Alignment",
                      value="Humans tend toward no particular alignment. The best and the worst are found among them.",
                      inline=False)
embed_human.add_field(name="Size",
                      value="Humans vary widely in height and build, from barely 5 feet to well over 6 feet tall. Regardless of your position in that range, your size is Medium.",
                      inline=False)
embed_human.add_field(name="Speed",
                      value="Your base walking speed is 30 feet.",
                      inline=False)
embed_human.add_field(name="Languages",
                      value="You can speak, read, and write Common and one extra language of your choice. Humans typically learn the languages of other peoples they deal with, including obscure dialects. They are fond of sprinkling their speech with words borrowed from other tongues: Orc curses, Elvish musical expressions, Dwarvish military phrases, and so on.",
                      inline=False)
