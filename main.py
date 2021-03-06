import os
from dotenv import load_dotenv
import json
import requests
import pandas as pd
import pickle
from datetime import datetime
from datetime import timedelta
from dateutil import parser
from dateutil.relativedelta import relativedelta

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
def getMessages(channelID, numRequests, preservePickle):
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
            last_message_id = df["id"][len(df.index) - 1]
            print(last_message_id)
            req = requests.get(
                f'https://discord.com/api/v9/channels/{channelID}/messages?limit=100&before={last_message_id}',
                headers=headers)
            message_dict[x] = json.loads(req.text)
            tmp_df = pd.DataFrame(message_dict[x])
            df = pd.concat([df, tmp_df], ignore_index=True)

    if (preservePickle == True):
        with open('pickleArtifact.txt', 'wb') as pickle_artifact:
            pickle.dump(obj=df, file=pickle_artifact)
        return df


def monthly_analysis(df_input: pd.DataFrame, start_year, start_month, start_day, start_hour=0, start_minute=0,
                     delta_years=0, delta_weeks=0, delta_days=0, delta_hours=1, delta_minutes=0):
    print("running monthly analysis")

    start_date = datetime.date(
        datetime(start_year, start_month, start_day, start_hour, start_minute)
    )

    delta: timedelta = timedelta(minutes=delta_minutes, hours=delta_hours, days=delta_days,
                                 weeks=delta_weeks + (52 * delta_years))

    end_date: datetime = start_date + delta;

    tester = "2022-05-24T14:23:28.770000+00:00"
    testerDate = datetime.strptime(tester, '%Y-%m-%dT%H:%M:%S.%f%z')
    print(testerDate.timestamp())

    df_input = df_input["timestamp"].apply(get_date)


def get_date(timestr: str):
    try:
        curDate: datetime = datetime.strptime(timestr, '%Y-%m-%dT%H:%M:%S.%f%z')
        print(curDate.date())

        return curDate
    except:
        curDate: datetime = parser.parse(timestr)

        return curDate



    # paramitze start date and interval length, use delta time
    # delta = relativeD`elta(months+=months, weeks+=weeks, days +=days, hours+=hours)
    # set defaults of zero for all these
    # end date = startdate + delta
    # use simple operators to compare


#  -----------------END-METHODS----------------------

#  -----------------RUNNING----------------------
# getMessages(channelID, 500)
pickle_to_open = open('pickleArtifact.txt', 'rb')
df = pickle.load(pickle_to_open)

monthly_analysis(df, start_year=2022, start_month=6, start_day=1, delta_years=1)

print('donzo')

#  -----------------END-RUN----------------------
