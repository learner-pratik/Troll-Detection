import os
import pickle
import csv
import requests
import json
from collections import defaultdict
# import facebook
import google.oauth2.credentials

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

CLIENT_SECRETS_FILE = "D:\hack\main\client_secret.json"
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
api_key = 'AIzaSyAVJcQ0549l7BnK62jvf3EnITtgeMJXuww'

def get_authenticated_service():
    credentials = None
    if os.path.exists('D:\hack\main\token.pickle'):
        with open('D:\hack\main\token.pickle', 'rb') as token:
            credentials = pickle.load(token)
    #  Check if the credentials are invalid or do not exist
    if not credentials or not credentials.valid:
        # Check if the credentials have expired
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE, SCOPES)
            credentials = flow.run_console()

        # Save the credentials for the next run
        with open('D:\hack\main\token.pickle', 'wb') as token:
            pickle.dump(credentials, token)

    return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

username = []

def get_video_comments(service, **kwargs):
    comments = []
    results = service.commentThreads().list(**kwargs).execute()
    for item in results['items']:
        print(item)
        print()
        print()
    while results:
        for item in results['items']:
            username.append(item['snippet']['topLevelComment']['snippet']['authorDisplayName'])
            comment_id = item['snippet']['topLevelComment']['id']
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            l = [comment_id, comment]
            comments.append(l)

        if 'nextPageToken' in results:
            kwargs['pageToken'] = results['nextPageToken']
            results = service.commentThreads().list(**kwargs).execute()
        else:
            break

    return comments

# def write_to_csv(comments):
#     with open('comments1.csv', 'w') as comments_file:
#         comments_writer = csv.writer(comments_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#         comments_writer.writerow(['Video ID', 'Title', 'Username', 'Comment'])
#         for row in comments:
#             comments_writer.writerow(list(row))

def get_my_uploads_list(service):
    # Retrieve the contentDetails part of the channel resource for the
    # authenticated user's channel.
    channels_response = service.channels().list(
        mine=True,
        part='contentDetails'
    ).execute()

    for channel in channels_response['items']:
        # From the API response, extract the playlist ID that identifies the list
        # of videos uploaded to the authenticated user's channel.
        return channel['contentDetails']['relatedPlaylists']['uploads']

    return None

data=defaultdict(list)

def list_my_uploaded_videos(service, uploads_playlist_id):
    
    # Retrieve the list of videos uploaded to the authenticated user's channel.
    url = ('https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze' + '?key=' + api_key)

    playlistitems_list_request = service.playlistItems().list(
        playlistId=uploads_playlist_id,
        part='snippet',
        maxResults=5
    )
    # print(playlistitems_list_request)
    # print 'Videos in list %s' % uploads_playlist_id
    final_result = []
    troll_responses = []
    while playlistitems_list_request:
        playlistitems_list_response = playlistitems_list_request.execute()
        # print(playlistitems_list_response)
        # Print information about each video.
        for playlist_item in playlistitems_list_response['items']:
            title = playlist_item['snippet']['title']
            # print(title)
            video_id = playlist_item['snippet']['resourceId']['videoId']
            # print(video_id)
            # print '%s (%s)' % (title, video_id)
            comments = get_video_comments(service, part='snippet', videoId=video_id, textFormat='plainText')
            # print(comments)

            for i in range(len(comments)):
                data_dict = {}
                data_dict['comment'] = {}
                data_dict['comment']['text'] = comments[i][1]
                data_dict['languages'] = ['en']
                data_dict['requestedAttributes'] = {}
                data_dict['requestedAttributes']['TOXICITY'] = {}

                # print(data_dict)

                response = requests.post(url=url, data=json.dumps(data_dict)) 
                # print(count)
                # count += 1
                # time.sleep(1)
                response_dict = json.loads(response.content)
                troll_responses.append(response_dict)
                # print(data_dict['comment']['text'])
                # print()
                # print(json.dumps(response_dict, indent=2))
                # print("------------------------------------------------------")


            final_result.extend([(video_id, title, comment) for comment in comments])
        
        playlistitems_list_request = service.playlistItems().list_next(playlistitems_list_request, playlistitems_list_response)
    
    # print(troll_responses)
    file = open('D:\hack\main\delete_msg.txt', 'w')
    print(len(troll_responses))
    x = len(comments)
    for i in range(len(troll_responses)):
        if x==0:
            break
        print(i)
        # print(comments[i][1])
        val = troll_responses[i]['attributeScores']['TOXICITY']['summaryScore']['value']
        print(val)
        # print(message[i])
        # print(val)
        if val*100 > 80:
            # file.write(comments[i][1]+'\n')
            file.write(username[i]+' | '+comments[i][1]+'\n')
            data[username[i]].append(comments[i][1])
            # delelte_comment(service, comments[i][0])
        x -= 1
    file.close()
    return(data)

    # write_to_csv(final_result)   
        # playlistitems_list_request = youtube.playlistItems().list_next(
        # playlistitems_list_request, playlistitems_list_response)

def delelte_comment(service, comment_id):
    request = service.comments().setModerationStatus(
        id=comment_id,
        moderationStatus="published",
        banAuthor=False
    )
    request.execute()

def getyoutube():
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    service = get_authenticated_service()
    uploads_playlist_id = get_my_uploads_list(service)
    # print(uploads_playlist_id)
    data=list_my_uploaded_videos(service, uploads_playlist_id)
    return(data)
# if __name__ == '__main__':
    # When running locally, disable OAuthlib's HTTPs verification. When
    # running in production *do not* leave this option enabled.
    # os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    # service = get_authenticated_service()
    # uploads_playlist_id = get_my_uploads_list(service)
    # # print(uploads_playlist_id)
    # list_my_uploaded_videos(service, uploads_playlist_id)
    # delelte_comment(service)
    # service.comments().delete(id='ZciQmtWTN6k').execute()
    # search_videos_by_keyword(get_my_uploads_list(service))
    # keyword = input('Enter a keyword: ')
    # search_videos_by_keyword(service, q=keyword, part='id,snippet', eventType='completed', type='video')