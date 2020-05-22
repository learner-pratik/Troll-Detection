#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Use text editor to edit the script and type in valid Instagram username/password
from collections import defaultdict
from InstagramAPI import InstagramAPI
import time
import json 
import requests 
from datetime import datetime
def getinsta():
    count=0
    while(count<10):
        count+=1
        media_id = []

        # stop conditions, the script will end when first of them will be true
        until_date = '2017-03-31'
        count = 100

        API = InstagramAPI("IG_USERNAME", "IG_PASSWORD")
        # time.sleep(15)
        API.login()
        # API.getSelfUserFeed()  # get self user feed
        # print(API.LastJson)  # print last response JSON
        API.getSelfUserFeed()
        for i in API.LastJson['items']:
            media_id.append(i['id'])
        API.getSelfUsernameInfo()
        print(media_id)
        has_more_comments = True
        max_id = ''
        dpost=defaultdict(list)
        delmes={}
        s=[]
        s=set(s)
        # comments_main=[]

        for i in media_id:
            comments = []
            has_more_comments = True
            max_id = ''
            print(i)
            while has_more_comments:
                print(max_id)
                _ = API.getMediaComments(i, max_id=max_id)
                # comments' page come from older to newer, lets preserve desc order in full list
                # print(API.LastJson['comments'])
                for c in reversed(API.LastJson['comments']):
                    comments.append(c)
                    print(c['text'])
                    if c['pk'] not in s:
                        dpost[i].append([c['pk'],c['text'],c['user']['username']])
                        s.add(c['pk'])
                has_more_comments = API.LastJson.get('has_more_comments', False)
                # evaluate stop conditions
                if count and len(comments) >= count:
                    comments = comments[:count]
                    # stop loop
                    has_more_comments = False
                    print ("stopped by count")
                if until_date:
                    older_comment = comments[-1]
                    dt = datetime.utcfromtimestamp(older_comment.get('created_at_utc', 0))
                    # only check all records if the last is older than stop condition
                    if dt.isoformat() <= until_date:
                        # keep comments after until_date
                        comments = [
                            c
                            for c in comments
                            if datetime.utcfromtimestamp(c.get('created_at_utc', 0)) > until_date
                        ]
                        # stop loop
                        has_more_comments = False
                        print ("stopped by until_date")
                # next page
                if has_more_comments:
                    max_id = API.LastJson.get('next_max_id', '')
                    time.sleep(2)
            # comments_main.append(comments)
            # print(comments)
            print(35*'_')

        print(dpost)
        # print(comments[0]['text'],comments[0]['user']['full_name'])

        api_key = 'AIzaSyAVJcQ0549l7BnK62jvf3EnITtgeMJXuww'
        url = ('https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze' +    
            '?key=' + api_key)
        for i in dpost.keys():
            for j in dpost[i]:
                data_dict = {
                    'comment': {'text': j[1]},
                    'languages': ['en'],
                    'requestedAttributes': {'TOXICITY': {}}
                }
                response = requests.post(url=url, data=json.dumps(data_dict)) 
                response_dict = json.loads(response.content)
                # print(response_dict['attributeScores'])
                j.append(response_dict['attributeScores']['TOXICITY']['summaryScore']['value']) 
                print(json.dumps(response_dict, indent=2))
        print(dpost)

        #####################delete
        for i in dpost.keys():
            for j in dpost[i]:
                if j[3]>0.6:
                    delmes[i]=j
                    API.deleteComment(i,j[0])
                    del(j)
        ret=delmes
    return(ret)
