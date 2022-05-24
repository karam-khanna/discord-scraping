import os
from dotenv import load_dotenv
import json
import requests
import pandas as pd


#  -----------------SET UP----------------------
load_dotenv()
# set up vars
auth = os.getenv('AUTHORIZATION')
channelID = 875443001579671555
# https://discord.com/api/v9/channels/875443001579671555/messages?limit=50

headers = {
    'authorization': auth
}
#  -----------------END-SETUP----------------------
#  -----------------DEFINE METHODS----------------------
# goals: get the last thousand messages
def getMessages(channelID):
    # request messages
    df = pd.DataFrame()
    message_dict = {}

    for x in range(100):
        if (x == 0):
            req = requests.get(f'https://discord.com/api/v9/channels/{channelID}/messages?limit=100', headers=headers)
            message_dict[x] = json.loads(req.text)
            df = pd.DataFrame(message_dict[x])
            with open('dataDump.json', 'w') as convert_file:
                convert_file.write(json.dumps(message_dict))
        else:
            last_message_id = df["id"][len(df.index)-1]
            print(last_message_id)
            req = requests.get(f'https://discord.com/api/v9/channels/{channelID}/messages?limit=100&before={last_message_id}', headers=headers)
            message_dict[x] = json.loads(req.text)
            tmp_df = pd.DataFrame(message_dict[x])
            df = pd.concat([df, tmp_df], ignore_index=True)

    # df = pd.DataFrame(columns= ['Content', 'Sender', 'TimeStamp'])


    # df = pd.concat([df, df2], ignore_index=True)
    return df



#  -----------------END-METHODS----------------------

#  -----------------RUNNING----------------------
df = getMessages(channelID)



print('donzo')



#  -----------------END-RUN----------------------
