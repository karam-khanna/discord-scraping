import os
from dotenv import load_dotenv
import json
import requests
import pandas as pd
import pickle


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
def getMessages(channelID, numRequests):
    # request messages
    df = pd.DataFrame()
    message_dict = {}

    for x in range(numRequests):
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


    with open ('pickleArtifact.txt', 'wb') as pickle_artifact:
        pickle.dump(obj=df, file=pickle_artifact)
    return df



#  -----------------END-METHODS----------------------

#  -----------------RUNNING----------------------
# getMessages(channelID, 500)
pickle_to_open = open('pickleArtifact.txt', 'rb')
df = pickle.load(pickle_to_open)


print('donzo')



#  -----------------END-RUN----------------------
