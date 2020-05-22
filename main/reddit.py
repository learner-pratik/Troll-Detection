import praw
import time
import requests
import json
from collections import defaultdict

def getreddit():
    reddit = praw.Reddit(client_id='CLIENT_ID',
                        client_secret='CLIENT_SECRET',
                        password='PASSWORD',
                        user_agent='my user agent',
                        username='USERNAME'
                        )

    print(reddit.user.me())
    # while(True):
    par = {}
    data = defaultdict(list)
    res = {}
    dele = []
    # print(reddit.user.preferences())
    # print(reddit.user.subreddits())
    for comment in reddit.redditor('USERNAME').comments.new(limit=None):
        print(comment.author)
        par[comment.parent_id] = comment.id
        data[comment.id].append(comment.body)
        data[comment.id].append(comment.author.name)
        res[comment.id] = 0
        # a=comment.id
    # reddit.read_only = True
    print(reddit.read_only)
    api_key = 'AIzaSyAVJcQ0549l7BnK62jvf3EnITtgeMJXuww'
    url = ('https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze' +
            '?key=' + api_key)
    for i in data.keys():
        data_dict = {
            'comment': {'text': data[i][0]},
            'languages': ['en'],
            'requestedAttributes': {'TOXICITY': {}}
        }
        response = requests.post(url=url, data=json.dumps(data_dict))
        print(response)
        response_dict = json.loads(response.content)
        # print(response_dict['attributeScores'])
        res[i] = response_dict['attributeScores']['TOXICITY']['summaryScore']['value']
        print(json.dumps(response_dict, indent=2))
    print(data)
    print(res)
    for i in res.keys():
        if res[i] > 0.6:
            comment = reddit.comment(i)
            dele.append([data[i][1],data[i][0]])
            comment.delete()
    print(dele,'delete')
    return(dele)
# subreddit=reddit.subreddit('news')
# hot_python = subreddit.hot()
# for submission in hot_python:
#     print(submission.title)

# for comment in reddit.redditor('ravinalawade').comments.new(limit=None):
#     print(comment.id,comment.body)
# delete
# comment = reddit.comment(a)
# comment.delete()
#######################

# for comment in reddit.redditor('ravinalawade').comments.new(limit=None):
#     print(comment.id,comment.body)
# conversedict={}
# hot_python = subreddit.hot(limit=3)
# for submission in hot_python:
#     if not submission.stickied:
#         print('Title: {}, ups: {}, downs: {}, Have we visited?: {}, subid: {}'.format(submission.title,
#                                                                                                    submission.ups,
#                                                                                                    submission.downs,
#                                                                                                    submission.visited,
#                                                                                                    submission.id))

#         submission.comments.replace_more(limit=0)
#         for comment in submission.comments.list():
#             if comment.id not in conversedict:
#                 conversedict[comment.id] = [comment.body,{}]
#                 if comment.parent() != submission.id:
#                     parent = str(comment.parent())
#                     conversedict[parent][1][comment.id] = [comment.ups, comment.body]


# Dictionary Format#
'''
conversedict = {post_id: [parent_content, {reply_id:[votes, reply_content],
                                            reply_id:[votes, reply_content],
                                            reply_id:[votes, reply_content]}],

                post_id: [parent_content, {reply_id:[votes, reply_content],
                                            reply_id:[votes, reply_content],
                                            reply_id:[votes, reply_content]}],
                                            
                post_id: [parent_content, {reply_id:[votes, reply_content],
                                            reply_id:[votes, reply_content],
                                            reply_id:[votes, reply_content]}],
                }


'''

# for post_id in conversedict:
#     message = conversedict[post_id][0]
#     replies = conversedict[post_id][1]
#     if len(replies) > 1:
#         print('Original Message: {}'.format(message))
#         print(35*'_')
#         print('Replies:')
#         for reply in replies:
#             print(replies[reply])
# print(len(conversedict.keys()))
