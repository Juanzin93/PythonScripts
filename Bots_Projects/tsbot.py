#!/usr/bin/python3
## BORA DE TS BOT PORRAAAAAA
#imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import ts3
from datetime import timedelta, datetime
from time import sleep
import threading
import sqlite3
from natsort import natsorted

connect = sqlite3.connect('KingdomSwapTSBot.db')
cursor = connect.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS EnemiesGuild(
    id integer PRIMARY KEY, name TEXT)
    ''')
cursor.execute('''CREATE TABLE IF NOT EXISTS EnemyMakersGuild(
    id integer PRIMARY KEY, name TEXT)
    ''')
cursor.execute('''CREATE TABLE IF NOT EXISTS FriendsGuild(
    id integer PRIMARY KEY, name TEXT)
    ''')
cursor.execute('''CREATE TABLE IF NOT EXISTS FriendMakersGuild(
    id integer PRIMARY KEY, name TEXT)
    ''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Enemies(
    id integer PRIMARY KEY, name TEXT, level TEXT, vocation TEXT, guild TEXT, death TEXT)
    ''')
cursor.execute('''CREATE TABLE IF NOT EXISTS EnemyMakers(
    id integer PRIMARY KEY, name TEXT, level TEXT, vocation TEXT, guild TEXT, death TEXT)
    ''')
cursor.execute('''CREATE TABLE IF NOT EXISTS Friends(
    id integer PRIMARY KEY, name TEXT, level TEXT, vocation TEXT, guild TEXT, death TEXT)
    ''')
cursor.execute('''CREATE TABLE IF NOT EXISTS FriendMakers(
    id integer PRIMARY KEY, name TEXT, level TEXT, vocation TEXT, guild TEXT, death TEXT)
    ''')
cursor.execute('''CREATE TABLE IF NOT EXISTS Hunteds(
    id integer PRIMARY KEY, name TEXT, level TEXT, vocation TEXT, guild TEXT, death TEXT)
    ''')

chrome_Options = Options()
#chrome_Options.add_argument("--headless")
PATH = r"chromedriver.exe"
CHROME_PATH = r"C:/Program Files/Google/Chrome/Application/chrome.exe"
chrome_Options.binary_location = CHROME_PATH

class TsBot:
    def __init__(self, **kwargs):
        self.ts3conn = ts3.query.TS3ServerConnection("telnet://serveradmin:kfdeJCAd2CNJ@68.205.37.3:10101")
        self.ts3conn.exec_("use", sid=2)
        self.ts3conn.exec_("clientupdate", client_nickname="RRABot")
        resp = self.ts3conn.exec_("whoami")
        self.ts3conn.exec_("clientmove", clid=resp.parsed[0]["client_id"], cid=41)
        
    def updateGuildMembersInDatabase(self):
        cursor.execute("SELECT name FROM EnemiesGuild")
        enemyguildname = [x[0] for x in cursor.fetchall()]
        print(enemyguildname)
        for enemieGuild in enemyguildname:
            enemyGuildSite = webdriver.Chrome(executable_path=PATH, options=chrome_Options)          

            splitenemyGuildName = enemieGuild.split()
            enemyGuild = "%20".join(splitenemyGuildName)
            enemyGuilds = f"https://ocpaweb.ocpafl.org/parcelsearch"

            enemyGuildSite.get(enemyGuilds)
            enemyguildsize = len(enemyGuildSite.find_elements_by_xpath(("//table[@id='guildViewTable']/tbody/tr")))
            for i in range(2, enemyguildsize+ 1, 1):
                Enemyplayer = enemyGuildSite.find_element_by_xpath((f"//table[@id='guildViewTable']/tbody/tr[{i}]/td[2]/a"))
                Enemielevel = enemyGuildSite.find_element_by_xpath((f"//table[@id='guildViewTable']/tbody/tr[{i}]/td[3]"))
                Enemievocation = enemyGuildSite.find_element_by_xpath((f"//table[@id='guildViewTable']/tbody/tr[{i}]/td[4]"))
                cursor.execute('''SELECT * FROM Enemies WHERE name = ?''', [Enemyplayer.text])
                if cursor.fetchone() is None:
                    cursor.execute('''INSERT INTO Enemies(name, level, vocation, guild) VALUES(?,?,?,?)''', (Enemyplayer.text, Enemielevel.text, Enemievocation.text, enemieGuild))
                    connect.commit()
            enemyGuildSite.close()

        cursor.execute("SELECT name FROM EnemyMakersGuild")
        enemyguildmakersname = [x[0] for x in cursor.fetchall()]
        for enemymakerGuild in enemyguildmakersname:
            enemymakersGuildSite = webdriver.Chrome(executable_path=PATH, options=chrome_Options)

            splitenemymakersGuildName = enemymakerGuild.split()
            enemymakersGuild = "%20".join(splitenemymakersGuildName)
            enemymakersGuilds = f"https://kingdom-swap.com/guilds.php?name={enemymakersGuild}"
            enemymakersGuildSite.get(enemymakersGuilds)
            enemymakersguildsize = len(enemymakersGuildSite.find_elements_by_xpath(("//table[@id='guildViewTable']/tbody/tr")))
            for i in range(2, enemymakersguildsize+ 1, 1):
                Enemymakersplayer = enemymakersGuildSite.find_element_by_xpath((f"//table[@id='guildViewTable']/tbody/tr[{i}]/td[2]/a"))
                Enemiemakerslevel = enemymakersGuildSite.find_element_by_xpath((f"//table[@id='guildViewTable']/tbody/tr[{i}]/td[3]"))
                Enemiemakersvocation = enemymakersGuildSite.find_element_by_xpath((f"//table[@id='guildViewTable']/tbody/tr[{i}]/td[4]"))
                cursor.execute('''SELECT * FROM EnemyMakers WHERE name = ?''', [Enemymakersplayer.text])
                if cursor.fetchone() is None:
                    cursor.execute('''INSERT INTO EnemyMakers(name, level, vocation, guild) VALUES(?,?,?,?)''', (Enemymakersplayer.text, Enemiemakerslevel.text, Enemiemakersvocation.text, enemymakerGuild))
                    connect.commit()
            enemymakersGuildSite.close()

        cursor.execute("SELECT name FROM FriendsGuild")
        friendguildname = [x[0] for x in cursor.fetchall()]
        print(friendguildname)
        #["Red Ribbon Army", "Total War", "Latin Kings PVP", "Peaky Blinders CO", "Unidos Contra Power Abuse"]
        for friendsGuild in friendguildname:
            friendGuildSite = webdriver.Chrome(executable_path=PATH, options=chrome_Options)
            print(friendsGuild)
            splitfriendGuildName = friendsGuild.split()
            friendGuild = "%20".join(splitfriendGuildName)
            friendGuilds = f"https://kingdom-swap.com/guilds.php?name={friendGuild}"
            friendGuildSite.get(friendGuilds)
            friendsguildsize = len(friendGuildSite.find_elements_by_xpath(("//table[@id='guildViewTable']/tbody/tr")))
            for i in range(2, friendsguildsize+ 1, 1):
                Friendplayer = friendGuildSite.find_element_by_xpath((f"//table[@id='guildViewTable']/tbody/tr[{i}]/td[2]/a"))
                Friendlevel = friendGuildSite.find_element_by_xpath((f"//table[@id='guildViewTable']/tbody/tr[{i}]/td[3]"))
                Friendvocation = friendGuildSite.find_element_by_xpath((f"//table[@id='guildViewTable']/tbody/tr[{i}]/td[4]"))
                cursor.execute('''SELECT * FROM Friends WHERE name = ?''', [Friendplayer.text])
                if cursor.fetchone() is None:
                    cursor.execute('''INSERT INTO Friends(name, level, vocation, guild) VALUES(?,?,?,?)''', (Friendplayer.text, Friendlevel.text, Friendvocation.text, friendsGuild))
                    connect.commit()
            friendGuildSite.close()

        self.ts3conn.send_keepalive()
        #try:
        #    
        #    event = self.ts3conn.wait_for_event(timeout=1)
        #except ts3.query.TS3TimeoutError or ts3.query.TS3TransportError:
        #    pass
        #else:
        #    print(event[0])
        cursor.execute("""SELECT name FROM FriendMakersGuild""")
        friendMakersguildname = [x[0] for x in cursor.fetchall()]
        for friendsMakersGuild in friendMakersguildname:
            friendMakersGuildSite = webdriver.Chrome(executable_path=PATH, options=chrome_Options)

            splitfriendMakersGuildName = friendsMakersGuild.split()
            friendMakersGuild = "%20".join(splitfriendMakersGuildName)
            friendMakersGuilds = f"https://kingdom-swap.com/guilds.php?name={friendMakersGuild}"
            friendMakersGuildSite.get(friendMakersGuilds)
            friendsMakersguildsize = len(friendMakersGuildSite.find_elements_by_xpath(("//table[@id='guildViewTable']/tbody/tr")))
            for i in range(2, friendsMakersguildsize+ 1, 1):
                FriendMakersplayer = friendMakersGuildSite.find_element_by_xpath((f"//table[@id='guildViewTable']/tbody/tr[{i}]/td[2]/a"))
                FriendMakerslevel = friendMakersGuildSite.find_element_by_xpath((f"//table[@id='guildViewTable']/tbody/tr[{i}]/td[3]"))
                FriendMakersvocation = friendMakersGuildSite.find_element_by_xpath((f"//table[@id='guildViewTable']/tbody/tr[{i}]/td[4]"))
                cursor.execute('''SELECT * FROM FriendMakers WHERE name = ?''', [FriendMakersplayer.text])
                if cursor.fetchone() is None:
                    cursor.execute('''INSERT INTO FriendMakers(name, level, vocation, guild) VALUES(?,?,?,?)''', (FriendMakersplayer.text, FriendMakerslevel.text, FriendMakersvocation.text, friendsMakersGuild))
                    connect.commit()
            friendMakersGuildSite.close()

        cursor.execute("""SELECT name FROM Hunteds""")
        Hunteds = [x[0] for x in cursor.fetchall()]
        #["Sharp Bolt", "Forrozin", "Shantos", "Firs Sativa", "Sir Petreca",
        #             "Mr Math", "Skillzao The Father", "Osirus Chappelle", "Ganondorf",
        #              "Miyamoto Musashi", "Pedro Luz", "Babydoge Tothemoon",
        #               "Greijal", "Malefian Death",
        #                "Like", "Schwarzenegger", "Servetti",
        #                 "Jorginho The Archer", "Pala Rush", "Kim Of Hell", "Ozzy",
        #                  "Draken Axe", "Epic Zan", "Green Backpack", "Cocaina",
        #                   "Insert Name Here", "Malafaia Mayhem"]
        for hunted in Hunteds:
            cursor.execute('''SELECT * FROM Hunteds WHERE name = ?''', [hunted])
            if cursor.fetchone() is None:
                huntedcharacter = webdriver.Chrome(executable_path=PATH, options=chrome_Options)
                huntedSplit = hunted.split()
                huntedName = "%20".join(huntedSplit)
                huntednamesite = f"https://kingdom-swap.com/characterprofile.php?name={huntedName}"
                huntedcharacter.get(huntednamesite)
                try:
                    huntedplayer = huntedcharacter.find_element_by_xpath((f"//div[@id='content']/h1"))
                    huntedlevel = huntedcharacter.find_element_by_xpath((f"//div[@id='content']/ul/li[contains(.,'Level: ')]"))
                    huntedvocation = huntedcharacter.find_element_by_xpath((f"//div[@id='content']/ul/li[contains(.,'Vocation: ')]"))
                    hunteddeath = huntedcharacter.find_elements_by_xpath(f"//div[@id='content']/ul/li[contains(.,'Killed at level')]")
                    huntedLevelSplit = str(huntedlevel.text).split("Level: ")
                    huntedVocationSplit = str(huntedvocation.text).split("Vocation: ")
                    if len(hunteddeath) > 0:
                        print(huntedplayer.text,huntedlevel.text,huntedvocation.text, hunteddeath[0].text)
                        cursor.execute('''INSERT INTO Hunteds(name, level, vocation, death) VALUES(?,?,?,?)''', (huntedplayer.text, huntedLevelSplit[1], huntedVocationSplit[1], hunteddeath[0].text))
                    else:
                        cursor.execute('''INSERT INTO Hunteds(name, level, vocation, death) VALUES(?,?,?,?)''', (huntedplayer.text, huntedLevelSplit[1], huntedVocationSplit[1], "This player has never died."))

                    connect.commit()
                except:
                    pass
                
                huntedcharacter.close()
            else:
                huntedcharacter = webdriver.Chrome(executable_path=PATH, options=chrome_Options)
                huntedSplit = hunted.split()
                huntedName = "%20".join(huntedSplit)
                huntednamesite = f"https://kingdom-swap.com/characterprofile.php?name={huntedName}"
                huntedcharacter.get(huntednamesite)
                huntedlevel = huntedcharacter.find_element_by_xpath((f"//div[@id='content']/ul/li[contains(.,'Level: ')]"))
                huntedlevelSplit = str(huntedlevel.text).split("Level: ")
                hunteddeath = huntedcharacter.find_elements_by_xpath(f"//div[@id='content']/ul/li[contains(.,'Killed at level')]")
                cursor.execute('''SELECT level FROM Hunteds WHERE name = ?''', [hunted])
                huntedLevel = [x[0] for x in cursor.fetchall()]
                print(huntedLevel[0])
                cursor.execute('''SELECT death FROM Hunteds WHERE name = ?''', [hunted])
                huntedDeath = [x[0] for x in cursor.fetchall()]
                print(huntedDeath[0])
                if len(hunteddeath) > 0:
                    hunteddeathSplit = str(hunteddeath[0].text).split(": ")

                    if str(hunteddeath[0].text) != str(huntedDeath[0]):
                        cursor.execute('''UPDATE Hunteds SET death = ? WHERE name = ?''', (hunteddeath[0].text, hunted))
                        connect.commit()
                        for client in self.ts3conn.exec_("clientlist"):
                            if client["client_type"] != "1" and client["client_type"] != "4":
                                self.ts3conn.exec_("clientpoke", clid=client["clid"], msg=f"[color=red][B] HUNTED : {hunted} {hunteddeathSplit[1]}[/color]")
                else:
                    pass
                if int(huntedLevel[0]) < int(huntedlevelSplit[1]):
                    cursor.execute('''UPDATE Hunteds SET level = ? WHERE name = ?''', (huntedlevelSplit[1], hunted))
                    connect.commit()
                    for client in self.ts3conn.exec_("clientlist"):
                        if client["client_type"] != "1" and client["client_type"] != "4":
                            self.ts3conn.exec_("clientpoke", clid=client["clid"] , msg=f"[B] [color=red][HUNTED][/color]: {hunted} Leveled Up to {huntedlevel.text}")  
                huntedcharacter.close()
        self.ts3conn.send_keepalive()
                
    def updatePlayersOnline(self):
        
        driver = webdriver.Chrome(executable_path=PATH, options=chrome_Options)
        # setup website
        websiteOnline = "https://kingdom-swap.com/onlinelist.php"
        driver.get(websiteOnline)
        # print title
        print("Connected to ", driver.title)
        NeutralsOnline = []
        NeutralsEk = []
        NeutralsEd = []
        NeutralsMs = []
        NeutralsRp = []
        NeutralsVc = []
        HuntedsEk = []
        HuntedsEd = []
        HuntedsMs = []
        HuntedsRp = []
        HuntedsVc = []
        cursor.execute('''SELECT * FROM Enemies''')
        Enemy = cursor.fetchall()
        EnemyOn = []
        EnemyEk = []
        EnemyEd = []
        EnemyMs = []
        EnemyRp = []
        EnemyVc = []
        cursor.execute('''SELECT * FROM EnemyMakers''')
        EnemyMakers = cursor.fetchall()
        EnemyMakersOn = []
        EnemyMakersEk = []
        EnemyMakersEd = []
        EnemyMakersMs = []
        EnemyMakersRp = []
        EnemyMakersVc = []
        cursor.execute('''SELECT * FROM Friends''')
        Friend = cursor.fetchall()
        FriendOn = []
        FriendEk = []
        FriendEd = []
        FriendMs = []
        FriendRp = []
        FriendVc = []
        cursor.execute('''SELECT * FROM FriendMakers''')
        FriendMakers = cursor.fetchall()
        FriendMakersOn = []
        FriendMakersEk = []
        FriendMakersEd = []
        FriendMakersMs = []
        FriendMakersRp = []
        FriendMakersVc = []
        cursor.execute('''SELECT * FROM Hunteds''')
        Hunteds = cursor.fetchall()
        HuntedsOnline = []
        playersOnlineTableSize = len(driver.find_elements_by_xpath(("//table[@class='table table-striped table-hover']/tbody/tr")))
        n = 0
        for i in range(2, playersOnlineTableSize+ 1, 1):
            n += 1
            if n == 100:
                self.ts3conn.send_keepalive()
                print("KeepAlive")

            if n == 200:
                self.ts3conn.send_keepalive()
                print("KeepAlive")
            
            if n == 300:
                self.ts3conn.send_keepalive()
                print("KeepAlive")
            
            if n == 400:
                self.ts3conn.send_keepalive()
                print("KeepAlive")

            if n == 500:
                self.ts3conn.send_keepalive()
                print("KeepAlive")

            if n == 600:
                self.ts3conn.send_keepalive()
                print("KeepAlive")

            player = driver.find_element_by_xpath((f"//table[@class='table table-striped table-hover']/tbody/tr[{i}]/td[1]"))
            guild = driver.find_element_by_xpath((f"//table[@class='table table-striped table-hover']/tbody/tr[{i}]/td[2]"))
            level = driver.find_element_by_xpath((f"//table[@class='table table-striped table-hover']/tbody/tr[{i}]/td[3]"))
            vocation = driver.find_element_by_xpath((f"//table[@class='table table-striped table-hover']/tbody/tr[{i}]/td[4]"))
            #print("entrou no if")
            neutros = f"{player.text} | {level.text} | {vocation.text} | {guild.text}"
            NeutralsOnline.append(neutros)
            print(neutros)
            if vocation.text == "Elite Knight" or vocation.text == "Knight":
                #print("entrou no ek")
                neutrokina = f"{level.text} {player.text} | {guild.text}"
                NeutralsEk.append(neutrokina)
            if vocation.text == "Elder Druid" or vocation.text == "Druid":
                #print("entrou no ed")
                neutrodruid = f"{level.text} {player.text} | {guild.text}"
                NeutralsEd.append(neutrodruid)
            if vocation.text == "Master Sorcerer" or vocation.text == "Sorcerer":
                #print("entrou no ms")
                neutrosorc = f"{level.text} {player.text} | {guild.text}"
                NeutralsMs.append(neutrosorc)
            if vocation.text == "Royal Paladin" or vocation.text == "Paladin":
                #print("entrou no rp")
                neutropally = f"{level.text} {player.text} | {guild.text}"
                NeutralsRp.append(neutropally)
            if vocation.text == "No vocation":
                #print("entrou no rp")
                neutroVc = f"{level.text} {player.text} | {guild.text}"
                NeutralsVc.append(neutroVc)

            for hunted in Hunteds:
                if player.text == hunted[1]:
                    HuntedsOnline.append(player.text + " | " + level.text + " | " + vocation.text + " | " + guild.text)
                    if vocation.text == "Elite Knight" or vocation.text == "Knight":
                        #print("entrou no ek")
                        Huntedskina = f"{level.text} {player.text} | {guild.text}"
                        HuntedsEk.append(Huntedskina)
                    if vocation.text == "Elder Druid" or vocation.text == "Druid":
                        #print("entrou no ed")
                        Huntedsdruid = f"{level.text} {player.text} | {guild.text}"
                        HuntedsEd.append(Huntedsdruid)
                    if vocation.text == "Master Sorcerer" or vocation.text == "Sorcerer":
                        #print("entrou no ms")
                        Huntedssorc = f"{level.text} {player.text} | {guild.text}"
                        HuntedsMs.append(Huntedssorc)
                    if vocation.text == "Royal Paladin" or vocation.text == "Paladin":
                        #print("entrou no rp")
                        Huntedspally = f"{level.text} {player.text} | {guild.text}"
                        HuntedsRp.append(Huntedspally)
                    if vocation.text == "No vocation":
                        #print("entrou no rp")
                        HuntedsVc = f"{level.text} {player.text} | {guild.text}"
                        HuntedsVc.append(HuntedsVc)

            for enemy in Enemy:
                if player.text == enemy[1]:
                    EnemyOn.append(player.text + " | " + level.text + " | " + vocation.text + " | " + guild.text)
                    if vocation.text == "Elite Knight" or vocation.text == "Knight":
                        #print("entrou no ek")
                        Enemykina = f"{level.text} {player.text} | {guild.text}"
                        EnemyEk.append(Enemykina)
                    if vocation.text == "Elder Druid" or vocation.text == "Druid":
                        #print("entrou no ed")
                        Enemydruid = f"{level.text} {player.text} | {guild.text}"
                        EnemyEd.append(Enemydruid)
                    if vocation.text == "Master Sorcerer" or vocation.text == "Sorcerer":
                        #print("entrou no ms")
                        EnemyMs.append(f"{level.text} {player.text} | {guild.text}")
                    if vocation.text == "Royal Paladin" or vocation.text == "Paladin":
                        #print("entrou no rp")
                        EnemyRp.append(f"{level.text} {player.text} | {guild.text}")
                    if vocation.text == "No vocation":
                        #print("entrou no rp")
                        EnemyVc.append(f"{level.text} {player.text} | {guild.text}")

            for enemyMakers in EnemyMakers:
                if player.text == enemyMakers[1]:
                    EnemyMakersOn.append(player.text + " | " + level.text + " | " + vocation.text + " | " + guild.text)
                    if vocation.text == "Elite Knight" or vocation.text == "Knight":
                        #print("entrou no ek")
                        EnemyMakerkina = f"{level.text} {player.text} | {guild.text}"
                        EnemyMakersEk.append(EnemyMakerkina)
                    if vocation.text == "Elder Druid" or vocation.text == "Druid":
                        #print("entrou no ed")
                        EnemyMakerdruid = f"{level.text} {player.text} | {guild.text}"
                        EnemyMakersEd .append(EnemyMakerdruid)
                    if vocation.text == "Master Sorcerer" or vocation.text == "Sorcerer":
                        #print("entrou no ms")
                        EnemyMakersMs.append(f"{level.text} {player.text} | {guild.text}")
                    if vocation.text == "Royal Paladin" or vocation.text == "Paladin":
                        #print("entrou no rp")
                        EnemyMakersRp.append(f"{level.text} {player.text} | {guild.text}")
                    if vocation.text == "No vocation":
                        #print("entrou no rp")
                        EnemyMakersVc.append(f"{level.text} {player.text} | {guild.text}")

            for friend in Friend:
                if player.text == friend[1]:
                    FriendOn.append(player.text + " | " + level.text + " | " + vocation.text + " | " + guild.text)
                    if vocation.text == "Elite Knight" or vocation.text == "Knight":
                        #print("entrou no ek")
                        Friendkina = f"{level.text} {player.text} | {guild.text}"
                        FriendEk.append(Friendkina)
                    if vocation.text == "Elder Druid" or vocation.text == "Druid":
                        #print("entrou no ed")
                        Frienddruid = f"{level.text} {player.text} | {guild.text}"
                        FriendEd.append(Frienddruid)
                    if vocation.text == "Master Sorcerer" or vocation.text == "Sorcerer":
                        #print("entrou no ms")
                        FriendMs.append(f"{level.text} {player.text} | {guild.text}")
                    if vocation.text == "Royal Paladin" or vocation.text == "Paladin":
                        #print("entrou no rp")
                        FriendRp.append(f"{level.text} {player.text} | {guild.text}")
                    if vocation.text == "No vocation":
                        #print("entrou no rp")
                        FriendVc.append(f"{level.text} {player.text} | {guild.text}")

            for friendMakers in FriendMakers:
                if player.text == friendMakers[1]:
                    FriendMakersOn.append(player.text + " | " + level.text + " | " + vocation.text + " | " + guild.text)
                    if vocation.text == "Elite Knight" or vocation.text == "Knight":
                        #print("entrou no ek")
                        FriendMakerkina = f"{level.text} {player.text} | {guild.text}"
                        FriendMakersEk.append(FriendMakerkina)
                    if vocation.text == "Elder Druid" or vocation.text == "Druid":
                        #print("entrou no ed")
                        FriendMakerdruid = f"{level.text} {player.text} | {guild.text}"
                        FriendMakersEd .append(FriendMakerdruid)
                    if vocation.text == "Master Sorcerer" or vocation.text == "Sorcerer":
                        #print("entrou no ms")
                        FriendMakersMs.append(f"{level.text} {player.text} | {guild.text}")
                    if vocation.text == "Royal Paladin" or vocation.text == "Paladin":
                        #print("entrou no rp")
                        FriendMakersRp.append(f"{level.text} {player.text} | {guild.text}")
                    if vocation.text == "No vocation":
                        #print("entrou no rp")
                        FriendMakersVc.append(f"{level.text} {player.text} | {guild.text}")
            
        sizeOfNeutralPlayersOnline = len(NeutralsOnline)
        sizeOfHuntedsOnline = len(HuntedsOnline)
        if sizeOfHuntedsOnline > 0:
            displayHuntedEks = "\n".join(natsorted(HuntedsEk, reverse=True))
            displayHuntedEds = "\n".join(natsorted(HuntedsEd, reverse=True))
            displayHuntedMss = "\n".join(natsorted(HuntedsMs, reverse=True))
            displayHuntedRps = "\n".join(natsorted(HuntedsRp, reverse=True))
            displayHuntedVcs = "\n".join(natsorted(HuntedsVc, reverse=True))
            displayHuntedsPlayers = f"""[img]https://i.imgur.com/sKqEwqU.png[/img]   Elite Knights:\n\n{displayHuntedEks}
                                    \n\n[img]https://i.imgur.com/qAXsL2J.png[/img]   Elder Druid:\n\n{displayHuntedEds}
                                    \n\n[img]https://i.imgur.com/Qmi5fzy.png[/img]   Master Sorcerer:\n\n{displayHuntedMss}
                                    \n\n[img]https://i.imgur.com/rYWmtmw.png[/img]   Royal Paladin:\n\n{displayHuntedRps}
                                    \n\n   No Vocation:\n\n{displayHuntedVcs}"""
        else:
            displayHuntedsPlayers = "No Hunteds Online."
        try:
            self.ts3conn.exec_(
                                "channeledit", cid=53,
                                channel_name=f"[cspacer]Hunteds ({sizeOfHuntedsOnline}/{len(Hunteds)})",
                                channel_description=displayHuntedsPlayers)
        except ts3.query.TS3QueryError:
            pass
        
        print("add os hunted")

        if sizeOfNeutralPlayersOnline > 0:
            displayNeutralEks = "\n".join(natsorted(NeutralsEk, reverse=True))
            displayNeutralEds = "\n".join(natsorted(NeutralsEd, reverse=True))
            displayNeutralMss = "\n".join(natsorted(NeutralsMs, reverse=True))
            displayNeutralRps = "\n".join(natsorted(NeutralsRp, reverse=True))
            displayNeutralVcs = "\n".join(natsorted(NeutralsVc, reverse=True))
            displayNeutralPlayers = f"""[img]https://i.imgur.com/sKqEwqU.png[/img]   Elite Knights:\n\n{displayNeutralEks}
                                    \n\n[img]https://i.imgur.com/qAXsL2J.png[/img]   Elder Druid:\n\n{displayNeutralEds}
                                    \n\n[img]https://i.imgur.com/Qmi5fzy.png[/img]   Master Sorcerer:\n\n{displayNeutralMss}
                                    \n\n[img]https://i.imgur.com/rYWmtmw.png[/img]   Royal Paladin:\n\n{displayNeutralRps}
                                    \n\n   No Vocation:\n\n{displayNeutralVcs}"""
        else:
            displayNeutralPlayers = "No Players Online."

        try:
            self.ts3conn.exec_(
                                "channeledit", cid=51, 
                                channel_name=f"[cspacer]Players Online ({sizeOfNeutralPlayersOnline})",
                                channel_description=displayNeutralPlayers)
        except ts3.query.TS3QueryError:
            pass

        print("add os neutral")


        sizeOfEnemyOnline = len(EnemyOn)
        if sizeOfEnemyOnline > 0:
            displayEnemyEks = "\n".join(natsorted(EnemyEk, reverse=True))
            displayEnemyEds = "\n".join(natsorted(EnemyEd, reverse=True))
            displayEnemyMss = "\n".join(natsorted(EnemyMs, reverse=True))
            displayEnemyRps = "\n".join(natsorted(EnemyRp, reverse=True))
            displayEnemyVcs = "\n".join(natsorted(EnemyVc, reverse=True))
            displayEnemyOnGuild = f"""[img]https://i.imgur.com/sKqEwqU.png[/img]   Elite Knights:\n\n{displayEnemyEks}
                                    \n\n[img]https://i.imgur.com/qAXsL2J.png[/img]   Elder Druid:\n\n{displayEnemyEds}
                                    \n\n[img]https://i.imgur.com/Qmi5fzy.png[/img]   Master Sorcerer:\n\n{displayEnemyMss}
                                    \n\n[img]https://i.imgur.com/rYWmtmw.png[/img]   Royal Paladin:\n\n{displayEnemyRps}
                                    \n\n   No Vocation:\n\n{displayEnemyVcs}"""
        else:
            displayEnemyOnGuild = "No Enemies Online."
        
        try:
            self.ts3conn.exec_(
                            "channeledit", cid=48,
                            channel_name=f"[cspacer]Enemies ({sizeOfEnemyOnline}/{len(Enemy)})",
                            channel_description=displayEnemyOnGuild)

        except ts3.query.TS3QueryError:
            pass
        
        print("add os enemy")

        sizeOfEnemyMakersOnline = len(EnemyMakersOn)
        if sizeOfEnemyMakersOnline > 0:
            displayEnemyMakerEks = "\n".join(natsorted(EnemyMakersEk, reverse=True))
            displayEnemyMakerEds = "\n".join(natsorted(EnemyMakersEd, reverse=True))
            displayEnemyMakerMss = "\n".join(natsorted(EnemyMakersMs, reverse=True))
            displayEnemyMakerRps = "\n".join(natsorted(EnemyMakersRp, reverse=True))
            displayEnemyMakerVcs = "\n".join(natsorted(EnemyMakersVc, reverse=True))
            displayEnemyMakersOnGuild = f"""[img]https://i.imgur.com/sKqEwqU.png[/img]   Elite Knights:\n\n{displayEnemyMakerEks}
                                    \n\n[img]https://i.imgur.com/qAXsL2J.png[/img]   Elder Druid:\n\n{displayEnemyMakerEds}
                                    \n\n[img]https://i.imgur.com/Qmi5fzy.png[/img]   Master Sorcerer:\n\n{displayEnemyMakerMss}
                                    \n\n[img]https://i.imgur.com/rYWmtmw.png[/img]   Royal Paladin:\n\n{displayEnemyMakerRps}
                                    \n\n   No Vocation:\n\n{displayEnemyMakerVcs}"""
        else:
            displayEnemyMakersOnGuild = "No Enemies Makers Online."
        
        try:
            self.ts3conn.exec_(
                            "channeledit", cid=49,
                            channel_name=f"[cspacer]Enemy makers ({sizeOfEnemyMakersOnline}/{len(EnemyMakers)})",
                            channel_description=displayEnemyMakersOnGuild)

        except ts3.query.TS3QueryError:
            pass

        print("add os enemy makers")

        sizeOfFriendOnline = len(FriendOn)
        if sizeOfFriendOnline > 0:
            displayFriendEks = "\n".join(natsorted(FriendEk, reverse=True))
            displayFriendEds = "\n".join(natsorted(FriendEd, reverse=True))
            displayFriendMss = "\n".join(natsorted(FriendMs, reverse=True))
            displayFriendRps = "\n".join(natsorted(FriendRp, reverse=True))
            displayFriendVcs = "\n".join(natsorted(FriendVc, reverse=True))
            displayFriendOnGuild = f"""[img]https://i.imgur.com/sKqEwqU.png[/img]   Elite Knights:\n\n{displayFriendEks}
                                    \n\n[img]https://i.imgur.com/qAXsL2J.png[/img]   Elder Druid:\n\n{displayFriendEds}
                                    \n\n[img]https://i.imgur.com/Qmi5fzy.png[/img]   Master Sorcerer:\n\n{displayFriendMss}
                                    \n\n[img]https://i.imgur.com/rYWmtmw.png[/img]   Royal Paladin:\n\n{displayFriendRps}
                                    \n\n   No Vocation:\n\n{displayFriendVcs}"""
        else:
            displayFriendOnGuild = "No Friends Online."
        
        try:
            self.ts3conn.exec_(
                            "channeledit", cid=50,
                            channel_name=f"[cspacer]Friends ({sizeOfFriendOnline}/{len(Friend)})",
                            channel_description=displayFriendOnGuild)

        except ts3.query.TS3QueryError:
            pass

        print("add os friend")
        
        sizeOfFriendMakersOnline = len(FriendMakersOn)
        if sizeOfFriendMakersOnline > 0:
            displayFriendMakerEks = "\n".join(natsorted(FriendMakersEk, reverse=True))
            displayFriendMakerEds = "\n".join(natsorted(FriendMakersEd, reverse=True))
            displayFriendMakerMss = "\n".join(natsorted(FriendMakersMs, reverse=True))
            displayFriendMakerRps = "\n".join(natsorted(FriendMakersRp, reverse=True))
            displayFriendMakerVcs = "\n".join(natsorted(FriendMakersVc, reverse=True))
            displayFriendMakersOnGuild = f"""[img]https://i.imgur.com/sKqEwqU.png[/img]   Elite Knights:\n\n{displayFriendMakerEks}
                                    \n\n[img]https://i.imgur.com/qAXsL2J.png[/img]   Elder Druid:\n\n{displayFriendMakerEds}
                                    \n\n[img]https://i.imgur.com/Qmi5fzy.png[/img]   Master Sorcerer:\n\n{displayFriendMakerMss}
                                    \n\n[img]https://i.imgur.com/rYWmtmw.png[/img]   Royal Paladin:\n\n{displayFriendMakerRps}
                                    \n\n   No Vocation:\n\n{displayFriendMakerVcs}"""
        else:
            displayFriendMakersOnGuild = "No Friend Makers Online."
        
        try:
            self.ts3conn.exec_(
                            "channeledit", cid=52,
                            channel_name=f"[cspacer]Friend makers ({sizeOfFriendMakersOnline}/{len(FriendMakers)})",
                            channel_description=displayFriendMakersOnGuild)

        except ts3.query.TS3QueryError:
            pass

        print("add os friend makers")
        
        driver.close()
        
if __name__ == "__main__":
    Bot = TsBot()
    Bot.__init__()   
    #threading.Thread(target=Bot.comandos).start()
    while True: 
        #Bot.updateGuildMembersInDatabase()
        #Bot.updatePlayersOnline()
