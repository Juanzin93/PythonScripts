
from fbchat import Client
from fbchat.models import *

client = Client("juanzin.usa@hotmail.com", "rionovo420")

# Fetches a list of all users you're currently chatting with, as `User` objects
users = client.fetchAllUsers()

print("users' IDs: {}".format([user.uid for user in users]))
print("users' names: {}".format([user.name for user in users]))


client.logout()