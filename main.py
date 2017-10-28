import requests
from pprint import pprint

# response = requests.get('https://jsonbin.io/b/59d0f30408be13271f7df29c').json()
# APP_ACCESS_TOKEN = response['access_token']


BASE_URL = 'https://api.instagram.com/v1/'
TOKEN = '4013952194.906cb6c.76bf3702386748f993f1d1d457549779'


def self_info():
    request_url = (BASE_URL + 'users/self/?access_token=%s') %(TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()
    # pprint(user_info)
    if user_info['meta']['code'] == 200:
        #print users details
        if 'data' in user_info:
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print "ERROR: Data not found!!"
    else:
        print 'Status code other than 200 received!'

# def get_info():
#     # END_POINT = '/users/self/'
#     # ACCESS_TOKEN = '?access_token={token}'.format(token=TOKEN)
#     user_info = requests.get(BASE_URL+END_POINT+ACCESS_TOKEN)
#     pprint(user_info.json())

self_info()