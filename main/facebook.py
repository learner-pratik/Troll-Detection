import facebook
import requests
import json

def getfbcomments():

    api_key = 'AIzaSyAVJcQ0549l7BnK62jvf3EnITtgeMJXuww'
    url = ('https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze' + '?key=' + api_key)

    graph = facebook.GraphAPI(access_token="ACCESS_TOKEN",version="3.1")

    pages_data = graph.get_object("/me/accounts")
    '''print(pages_data)'''

    page_id = '108525967430395'
    page_token = None
    for item in pages_data['data']:
        if item['id'] == page_id:
            page_token = item['access_token']      
            # print(page_token)

    posts_25 = graph.get_connections(id=page_id,connection_name='posts',)
    # print(posts_25['data'])
    post_comments = []
    post_comments_id = []
    troll_comments = []

    for post in posts_25['data']:
        msg = graph.get_connections(id=post['id'], connection_name='comments')
        print(msg)
        print()
        for comment in msg['data']:

            post_comments.append(comment['message'])
            post_comments_id.append(comment['id'])
            data_dict = {}
            data_dict['comment'] = {}
            data_dict['comment']['text'] = comment['message']
            data_dict['languages'] = ['en']
            data_dict['requestedAttributes'] = {}
            data_dict['requestedAttributes']['TOXICITY'] = {}

            response = requests.post(url=url, data=json.dumps(data_dict)) 
            # print(count)
            # count += 1
            # time.sleep(1)
            response_dict = json.loads(response.content)
            # print(comment['message'])
            # print(response_dict)
            troll_comments.append(response_dict)

    file = open('deleted_msgs', 'a')
    d = []
    for i in range(len(troll_comments)):
        val = troll_comments[i]['attributeScores']['TOXICITY']['summaryScore']['value']
        if val*100 > 60:
            url = "https://graph.facebook.com/"+post_comments_id[i]+"?access_token=PAGE_ACCESS_TOKEN&method=delete"
            payload = {}
            headers= {}
            response = requests.request("POST", url, headers=headers, data = payload)
            print(response.text.encode('utf8'))
            file.write(post_comments[i]+'\n')
            d.append(post_comments[i])
    file.close()

    return d