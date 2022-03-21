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

chrome_Options = Options()
chrome_Options.add_argument("--headless")
PATH = r"chromedriver.exe"
CHROME_PATH = r"C:/Program Files/Google/Chrome/Application/chrome.exe"
chrome_Options.binary_location = CHROME_PATH

connect = sqlite3.connect('KingdomSwapTSBot.db')
cursor = connect.cursor()

class TsBot:
    def __init__(self, **kwargs):
        self.ts3conn = ts3.query.TS3ServerConnection("telnet://serveradmin:kfdeJCAd2CNJ@68.205.37.3:10101")
        self.ts3conn.exec_("use", sid=2)
        self.ts3conn.exec_("clientupdate", client_nickname="RRABot.")
        resp = self.ts3conn.exec_("whoami")
        self.ts3conn.exec_("clientmove", clid=resp.parsed[0]["client_id"], cid=41)
        
        

    def comandos(self):
        #
        # Register for the event.
        try:
            self.ts3conn.exec_("servernotifyregister", event="textserver")

            recebido = self.ts3conn._recv(timeout=10)
        
            self.ts3conn.send_keepalive()
          
            comando = str(recebido.parsed[0]['msg']).split()
            msg = []
            for i in range(1, len(comando), 1):
                msg.append(comando[i])
            mensagem = " ".join(msg)
            print(recebido.parsed[0])
            if comando[0] == "!mp":
                print("comando MP")
                for client in self.ts3conn.exec_("clientlist"):
                    print(client)
                    if client['client_type'] != '1' and client["client_type"] != '4':
                        self.ts3conn.exec_("clientpoke", clid=client["clid"], msg=f"{recebido.parsed[0]['invokername']}: {mensagem}")  
                print("MassPoke enviado")
            
            if comando[0] == "!mk":
                for client in self.ts3conn.exec_("clientlist"):
                    if client['client_type'] != '1' and client['client_type'] != '0':
                        print(client)
                        if len(comando) > 1:
                            self.ts3conn.exec_("clientkick", clid=client["clid"], reasonid=5, reasonmsg=f"{recebido.parsed[0]['invokername']}: {mensagem}")
                        else:
                            self.ts3conn.exec_("clientkick", clid=client["clid"], reasonid=5, reasonmsg=f"{recebido.parsed[0]['invokername']}: {comando[1]}")    
            
            if comando[0] == "!mmove":
                print("comando Mmove")

                for client in self.ts3conn.exec_("clientlist"):
                    if str(client['client_nickname']) == str(recebido.parsed[0]['invokername']):
                        invokerchannel = client["cid"]
                for client in self.ts3conn.exec_("clientlist"):
                    if len(comando) > 1:
                        poke = []
                        for i in range(1, len(comando), 1):
                            poke.append(comando[i])
                        maspoke = " ".join(poke)
                        self.ts3conn.exec_("clientmove", clid=client["clid"], cid=invokerchannel)
                    else:
                        self.ts3conn.exec_("clientmove", clid=client["clid"], cid=invokerchannel)    

            if comando[0] == "!addenemyguild":
                cursor.execute(""" INSERT into EnemiesGuild (name) VALUES (?) """, (mensagem,))
                connect.commit()
                self.ts3conn.exec_("sendtextmessage", targetmode=3, msg=f"{mensagem} added to Enemy Guilds.")

            if comando[0] == "!addfriendguild":
                cursor.execute(""" INSERT into FriendsGuild (name) VALUES (?) """, (mensagem,))
                connect.commit()
                self.ts3conn.exec_("sendtextmessage", targetmode=3, msg=f"{mensagem} added to Friend Guilds.")
            
            if comando[0] == "!removeenemyguild":
                cursor.execute(""" DELETE from EnemiesGuild WHERE name = ? """, (mensagem,))
                connect.commit()
                self.ts3conn.exec_("sendtextmessage", targetmode=3, msg=f"{mensagem} removed from Enemy Guilds.")
            
            if comando[0] == "!removefriendguild":
                cursor.execute(""" DELETE from FriendsGuild WHERE name = ? """, (mensagem,))
                connect.commit()
                self.ts3conn.exec_("sendtextmessage", targetmode=3, msg=f"{mensagem} removed from Friend Guilds.")
            
            if comando[0] == "!addfriendmakersguild":
                cursor.execute(""" INSERT into FriendMakersGuild (name) VALUES (?) """, (comando[1],))
                connect.commit()
                self.ts3conn.exec_("sendtextmessage", targetmode=3, msg=f"{comando[1]} added to Friend Makers Guilds.")
        
            if comando[0] == "!removefriendmakersguild":
                cursor.execute(""" DELETE from FriendMakersGuild WHERE name = ? """, (comando[1],))
                connect.commit()
                self.ts3conn.exec_("sendtextmessage", targetmode=3, msg=f"{comando[1]} removed from Friend Makers Guilds.")
            
            if comando[0] == "!addenemymakersguild":
                cursor.execute(""" INSERT into EnemyMakersGuild (name) VALUES (?) """, (comando[1],))
                connect.commit()
                self.ts3conn.exec_("sendtextmessage", targetmode=3, msg=f"{comando[1]} added to Enemy Makers Guilds.")
            
            if comando[0] == "!removeenemymakersguild":
                cursor.execute(""" DELETE from EnemyMakersGuild WHERE name = ? """, (comando[1],))
                connect.commit()
                self.ts3conn.exec_("sendtextmessage", targetmode=3, msg=f"{comando[1]} removed from Enemy Makers Guilds.")
            
            if comando[0] == "!addfriend":
                cursor.execute('''SELECT * FROM Friends WHERE name = ?''', [mensagem])
                if cursor.fetchone() is None:
                    friendcharacter = webdriver.Chrome(executable_path=PATH, options=chrome_Options)
                    friendSplit = mensagem.split()
                    friendName = "%20".join(friendSplit)
                    friendnamesite = f"https://kingdom-swap.com/characterprofile.php?name={friendName}"
                    friendcharacter.get(friendnamesite)
                    try:
                        friendplayer = friendcharacter.find_element_by_xpath((f"//div[@id='content']/h1"))
                        friendlevel = friendcharacter.find_element_by_xpath((f"//div[@id='content']/ul/li[contains(.,'Level: ')]"))
                        friendvocation = friendcharacter.find_element_by_xpath((f"//div[@id='content']/ul/li[contains(.,'Vocation: ')]"))
                        try:
                            friendguild = friendcharacter.find_element_by_xpath((f"//div[@id='content']/ul/li[contains(.,'Guild: ')]"))
                            friendguildSplit = str(friendguild.text).split("Guild: ")

                        except:
                            pass
                        frienddeath = friendcharacter.find_elements_by_xpath(f"//div[@id='content']/ul/li[contains(.,'Killed at level')]")
                        friendLevelSplit = str(friendlevel.text).split("Level: ")
                        friendVocationSplit = str(friendvocation.text).split("Vocation: ")
                        if len(frienddeath) > 0:
                            try:
                                cursor.execute('''INSERT INTO Friends(name, level, vocation, guild, death) VALUES(?,?,?,?,?)''', (friendplayer.text, friendLevelSplit[1], friendVocationSplit[1], friendguildSplit[1].text, frienddeath[0].text))

                            except:
                                cursor.execute('''INSERT INTO Friends(name, level, vocation, death) VALUES(?,?,?,?)''', (friendplayer.text, friendLevelSplit[1], friendVocationSplit[1], frienddeath[0].text))
                        else:
                            try:
                                cursor.execute('''INSERT INTO Friends(name, level, vocation, guild, death) VALUES(?,?,?,?,?)''', (friendplayer.text, friendLevelSplit[1], friendVocationSplit[1], friendguildSplit[1].text, "This player has never died."))
                            except:
                                cursor.execute('''INSERT INTO Friends(name, level, vocation, death) VALUES(?,?,?,?)''', (friendplayer.text, friendLevelSplit[1], friendVocationSplit[1], "This player has never died."))

                        connect.commit()
                    except:
                        friendcharacter.close()
                        self.ts3conn.exec_("sendtextmessage", targetmode=3, msg=f"{mensagem} does not exist.")
                        return

                    
                    friendcharacter.close()
                    self.ts3conn.exec_("sendtextmessage", targetmode=3, msg=f"{mensagem} added to Friends.")
                else:
                    self.ts3conn.exec_("sendtextmessage", targetmode=3, msg=f"{mensagem} is already a friend.")
            if comando[0] == "!removefriend":
                cursor.execute(""" DELETE from Friends WHERE name = ? """, (mensagem,))
                connect.commit()
                self.ts3conn.exec_("sendtextmessage", targetmode=3, msg=f"{mensagem} removed from Friends.")

            if comando[0] == "!addenemy":
                cursor.execute('''SELECT * FROM Enemies WHERE name = ?''', [mensagem])
                if cursor.fetchone() is None:
                    enemycharacter = webdriver.Chrome(executable_path=PATH, options=chrome_Options)
                    enemySplit = mensagem.split()
                    enemyName = "%20".join(enemySplit)
                    enemynamesite = f"https://kingdom-swap.com/characterprofile.php?name={enemyName}"
                    enemycharacter.get(enemynamesite)
                    try:
                        enemyplayer = enemycharacter.find_element_by_xpath((f"//div[@id='content']/h1"))
                        enemylevel = enemycharacter.find_element_by_xpath((f"//div[@id='content']/ul/li[contains(.,'Level: ')]"))
                        enemyvocation = enemycharacter.find_element_by_xpath((f"//div[@id='content']/ul/li[contains(.,'Vocation: ')]"))
                        try:
                            enemyguild = enemycharacter.find_element_by_xpath((f"//div[@id='content']/ul/li[contains(.,'Guild: ')]"))
                            enemyguildSplit = str(enemyguild.text).split("Guild: ")

                        except:
                            pass
                        enemydeath = enemycharacter.find_elements_by_xpath(f"//div[@id='content']/ul/li[contains(.,'Killed at level')]")
                        enemyLevelSplit = str(enemylevel.text).split("Level: ")
                        enemyVocationSplit = str(enemyvocation.text).split("Vocation: ")
                        if len(enemydeath) > 0:
                            try:
                                cursor.execute('''INSERT INTO Enemies(name, level, vocation, guild, death) VALUES(?,?,?,?,?)''', (enemyplayer.text, enemyLevelSplit[1], enemyVocationSplit[1], enemyguildSplit[1].text, enemydeath[0].text))

                            except:
                                cursor.execute('''INSERT INTO Enemies(name, level, vocation, death) VALUES(?,?,?,?)''', (enemyplayer.text, enemyLevelSplit[1], enemyVocationSplit[1], enemydeath[0].text))
                        else:
                            try:
                                cursor.execute('''INSERT INTO Enemies(name, level, vocation, guild, death) VALUES(?,?,?,?,?)''', (enemyplayer.text, enemyLevelSplit[1], enemyVocationSplit[1], enemyguildSplit[1].text, "This player has never died."))
                            except:
                                cursor.execute('''INSERT INTO Enemies(name, level, vocation, death) VALUES(?,?,?,?)''', (enemyplayer.text, enemyLevelSplit[1], enemyVocationSplit[1], "This player has never died."))

                        connect.commit()
                    except:
                        enemycharacter.close()
                        self.ts3conn.exec_("sendtextmessage", targetmode=3, msg=f"{mensagem} does not exist.")
                        return

                    enemycharacter.close()
                    self.ts3conn.exec_("sendtextmessage", targetmode=3, msg=f"{mensagem} added to Enemies.")
                else:
                    self.ts3conn.exec_("sendtextmessage", targetmode=3, msg=f"{mensagem} already in Enemies.")

            if comando[0] == "!removeenemy":
                cursor.execute(""" DELETE from Enemies WHERE name = ? """, (mensagem,))
                connect.commit()
                self.ts3conn.exec_("sendtextmessage", targetmode=3, msg=f"{mensagem} removed from Enemies.")
            
            if comando[0] == "!addfriendmaker":
                cursor.execute('''SELECT * FROM FriendMakers WHERE name = ?''', [mensagem])
                if cursor.fetchone() is None:
                    friendMakerscharacter = webdriver.Chrome(executable_path=PATH, options=chrome_Options)
                    friendMakersSplit = mensagem.split()
                    friendMakersName = "%20".join(friendMakersSplit)
                    friendMakersnamesite = f"https://kingdom-swap.com/characterprofile.php?name={friendMakersName}"
                    friendMakerscharacter.get(friendMakersnamesite)
                    try:
                        friendMakersplayer = friendMakerscharacter.find_element_by_xpath((f"//div[@id='content']/h1"))
                        friendMakerslevel = friendMakerscharacter.find_element_by_xpath((f"//div[@id='content']/ul/li[contains(.,'Level: ')]"))
                        friendMakersvocation = friendMakerscharacter.find_element_by_xpath((f"//div[@id='content']/ul/li[contains(.,'Vocation: ')]"))
                        try:
                            friendMakersguild = friendMakerscharacter.find_element_by_xpath((f"//div[@id='content']/ul/li[contains(.,'Guild: ')]"))
                            friendMakersguildSplit = str(friendMakersguild.text).split("Guild: ")

                        except:
                            pass
                        friendMakersdeath = friendMakerscharacter.find_elements_by_xpath(f"//div[@id='content']/ul/li[contains(.,'Killed at level')]")
                        friendMakersLevelSplit = str(friendMakerslevel.text).split("Level: ")
                        friendMakersVocationSplit = str(friendMakersvocation.text).split("Vocation: ")
                        if len(friendMakersdeath) > 0:
                            try:
                                cursor.execute('''INSERT INTO FriendMakers(name, level, vocation, guild, death) VALUES(?,?,?,?,?)''', (friendMakersplayer.text, friendMakersLevelSplit[1], friendMakersVocationSplit[1], friendMakersguildSplit[1].text, friendMakersdeath[0].text))

                            except:
                                cursor.execute('''INSERT INTO FriendMakers(name, level, vocation, death) VALUES(?,?,?,?)''', (friendMakersplayer.text, friendMakersLevelSplit[1], friendMakersVocationSplit[1], friendMakersdeath[0].text))
                        else:
                            try:
                                cursor.execute('''INSERT INTO FriendMakers(name, level, vocation, guild, death) VALUES(?,?,?,?,?)''', (friendMakersplayer.text, friendMakersLevelSplit[1], friendMakersVocationSplit[1], friendMakersguildSplit[1].text, "This player has never died."))
                            except:
                                cursor.execute('''INSERT INTO FriendMakers(name, level, vocation, death) VALUES(?,?,?,?)''', (friendMakersplayer.text, friendMakersLevelSplit[1], friendMakersVocationSplit[1], "This player has never died."))

                        connect.commit()
                    except:
                        friendMakerscharacter.close()
                        self.ts3conn.exec_("sendtextmessage", targetmode=3, msg=f"{mensagem} does not exist.")
                        return

                    friendMakerscharacter.close()
                    self.ts3conn.exec_("sendtextmessage", targetmode=3, msg=f"{mensagem} added to Friend Makers.")
                else:
                    self.ts3conn.exec_("sendtextmessage", targetmode=3, msg=f"{mensagem} is already a Friend Maker.")
            
            if comando[0] == "!removefriendmaker":
                cursor.execute(""" DELETE from FriendMakers WHERE name = ? """, (mensagem,))
                connect.commit()
                self.ts3conn.exec_("sendtextmessage", targetmode=3, msg=f"{mensagem} removed from Friend Makers.")

            if comando[0] == "!addenemymaker":
                cursor.execute('''SELECT * FROM EnemyMakers WHERE name = ?''', [mensagem])
                print(mensagem)
                if cursor.fetchone() is None:
                    enemyMakerscharacter = webdriver.Chrome(executable_path=PATH, options=chrome_Options)
                    enemyMakersSplit = mensagem.split()
                    enemyMakersName = "%20".join(enemyMakersSplit)
                    enemyMakersnamesite = f"https://kingdom-swap.com/characterprofile.php?name={enemyMakersName}"
                    enemyMakerscharacter.get(enemyMakersnamesite)
                    try:
                        enemyMakersplayer = enemyMakerscharacter.find_element_by_xpath((f"//div[@id='content']/h1"))
                        enemyMakerslevel = enemyMakerscharacter.find_element_by_xpath((f"//div[@id='content']/ul/li[contains(.,'Level: ')]"))
                        enemyMakersvocation = enemyMakerscharacter.find_element_by_xpath((f"//div[@id='content']/ul/li[contains(.,'Vocation: ')]"))
                        try:
                            enemyMakersguild = enemyMakerscharacter.find_element_by_xpath((f"//div[@id='content']/ul/li[contains(.,'Guild: ')]"))
                            enemyMakersguildSplit = str(enemyMakersguild.text).split("Guild: ")
                        except:
                            pass
                        enemyMakersdeath = enemyMakerscharacter.find_elements_by_xpath(f"//div[@id='content']/ul/li[contains(.,'Killed at level')]")
                        enemyMakersLevelSplit = str(enemyMakerslevel.text).split("Level: ")
                        enemyMakersVocationSplit = str(enemyMakersvocation.text).split("Vocation: ")
                        if len(enemyMakersdeath) > 0:
                            try:
                                cursor.execute('''INSERT INTO EnemyMakers(name, level, vocation, guild, death) VALUES(?,?,?,?,?)''', (enemyMakersplayer.text, enemyMakersLevelSplit[1], enemyMakersVocationSplit[1], enemyMakersguildSplit[1].text, enemyMakersdeath[0].text))
                            except:
                                cursor.execute('''INSERT INTO EnemyMakers(name, level, vocation, death) VALUES(?,?,?,?)''', (enemyMakersplayer.text, enemyMakersLevelSplit[1], enemyMakersVocationSplit[1], enemyMakersdeath[0].text))
                        else:
                            try:
                                cursor.execute('''INSERT INTO EnemyMakers(name, level, vocation, guild, death) VALUES(?,?,?,?,?)''', (enemyMakersplayer.text, enemyMakersLevelSplit[1], enemyMakersVocationSplit[1], enemyMakersguildSplit[1].text, "This player has never died."))
                            except:
                                cursor.execute('''INSERT INTO EnemyMakers(name, level, vocation, death) VALUES(?,?,?,?)''', (enemyMakersplayer.text, enemyMakersLevelSplit[1], enemyMakersVocationSplit[1], "This player has never died."))

                        connect.commit()
                    except:
                        enemyMakerscharacter.close()
                        self.ts3conn.exec_("sendtextmessage", targetmode=3, msg=f"{mensagem} does not exist.")
                        return
                    
                    enemyMakerscharacter.close()
                    self.ts3conn.exec_("sendtextmessage", targetmode=3, msg=f"{mensagem} added to Enemy Makers.")
                else:
                    self.ts3conn.exec_("sendtextmessage", targetmode=3, msg=f"{mensagem} is already in Enemy Makers.")

            if comando[0] == "!removeenemymaker":
                cursor.execute(""" DELETE from EnemyMakers WHERE name = ? """, (mensagem,))
                connect.commit()
                self.ts3conn.exec_("sendtextmessage", targetmode=3, msg=f"{mensagem} removed from Enemy Makers.")
            
            if comando[0] == "!addhunted":
                cursor.execute(""" INSERT into Hunteds (name) VALUES (?) """, (mensagem,))
                connect.commit()
                self.ts3conn.exec_("sendtextmessage", targetmode=3, msg=f"{mensagem} added to Hunted.")

            self.ts3conn.exec_("servernotifyunregister", event="textprivate")
        except:
            pass
                
      
if __name__ == "__main__":
    Bot = TsBot()
    Bot.__init__()   
    while True: 
        Bot.comandos()
        
