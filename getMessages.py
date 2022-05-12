import os
from dotenv import load_dotenv
import json
import requests

load_dotenv()

# set up vars
auth = os.getenv('AUTHORIZATION')
channelID = 875443001579671555
# https://discord.com/api/v9/channels/875443001579671555/messages?limit=50

headers = {
    'authorization': auth
}


def getMessages(channelID):
    # request messages
    for x in range(6):
        req = requests.get(
            f'https://discord.com/api/v9/channels/{channelID}/messages?limit=100', headers=headers
        )
        messageDict[f'{x}'] = json.loads(req.text)

    print(len(messageDict["1"]))
    #
    # with open('dataDump.json', 'w') as convert_file:
    #     convert_file.write(json.dumps(messageDict))








getMessages(channelID)
