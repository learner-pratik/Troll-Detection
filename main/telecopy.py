import telepot
import pandas as pd
import csv
import requests
import json
import time


token = 'TOKEN'
chat_id = 'CHAT_ID'
api_key = 'AIzaSyAVJcQ0549l7BnK62jvf3EnITtgeMJXuww'

bot = telepot.Bot(token)
count = 1
# p = 1
while count<=60:
    print("Round1")
    message_id = []
    sender_id = []
    sender_name = []
    date = []
    message = []

    l = bot.getUpdates()
    # print(l)

    url = ('https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze' + '?key=' + api_key)

    file_name = 'deleted_msgs'
    file_lines = []
    with open(file_name, 'r') as read_obj:
        # Read all lines in the file one by one
        for line in read_obj:
            s = line.replace('\n', '')
            msgs = s.split(' | ')
            file_lines.append(msgs[2])

    # print(file_lines)
            
    for i in l:
        
        if 'message' in i.keys():
            if 'text' in i['message'].keys():
                if i['message']['text'] not in file_lines:
                    message.append(i['message']['text'])
                    # print(message)
                    if 'message_id' in i['message'].keys():
                        message_id.append(i['message']['message_id'])
                    if 'from' in i['message'].keys():
                        sender_id.append(i['message']['from']['id'])
                        sender_name.append(i['message']['from']['first_name']+" "+i['message']['from']['last_name'])
                        
                    if 'date' in i['message'].keys():
                        date.append(i['message']['date'])
                    
        else:
            continue

    troll_responses = []
    # print(message)

    for i in range(len(message)):
        data_dict = {}
        data_dict['comment'] = {}
        data_dict['comment']['text'] = message[i]
        data_dict['languages'] = ['en']
        data_dict['requestedAttributes'] = {}
        data_dict['requestedAttributes']['TOXICITY'] = {}

        # print(data_dict)

        response = requests.post(url=url, data=json.dumps(data_dict)) 
        # print(count)
        count += 1
        # time.sleep(1)
        response_dict = json.loads(response.content)
        troll_responses.append(response_dict)
        # print(data_dict)
        # print()
        # print(json.dumps(response_dict, indent=2))
        # print("------------------------------------------------------")

    for i in range(len(troll_responses)):
        val = troll_responses[i]['attributeScores']['TOXICITY']['summaryScore']['value']
        # print(message[i])
        # print(val)
        file = open('deleted_msgs', 'a')
        if val*100 > 80:
            print(message[i])
            print(message_id[i])
            bot.deleteMessage((chat_id, message_id[i]))
            # file.write(message[i]+'\n')
            file.write(str(sender_id[i])+' | '+sender_name[i]+' | '+message[i]+'\n')
        file.close()

    time.sleep(5)
    # p += 1