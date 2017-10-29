import requests
from pprint import pprint
import urllib

# response = requests.get('https://jsonbin.io/b/59d0f30408be13271f7df29c').json()
# APP_ACCESS_TOKEN = response['access_token']


BASE_URL = 'https://api.instagram.com/v1/'
TOKEN = '4013952194.906cb6c.76bf3702386748f993f1d1d457549779'
ACCESS_TOKEN = '?access_token={token}'.format(token=TOKEN)

def get_user_id(name):
    url = BASE_URL+ 'users/search?q={name}&access_token={token}'.format(name=name,token=TOKEN)
    response = requests.get(url).json()
    # pprint(response)
    if response['meta']['code'] == 200:
        if len(response['data']):
            return response['data'][0]['id']
        else:
            return None
    else:
        print 'Status code other than 200 received!'
        exit()


def get_user_post(username):
    user_id = get_user_id(username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = BASE_URL + "users/{userid}/media/recent/?access_token={token}".format(userid=user_id,token=TOKEN)
    user_media = requests.get(request_url).json()
    if user_media['meta']['code'] == 200:
        #extract post ID
        if len(user_media['data']):
            img_name = user_media['data'][0]['id']+'.jpeg'
            img_url = user_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(img_url,img_name)
            print "Your image has been saved"
        else:
            print "Post doesn't exist"
        # pprint(user_media['data'][0])
    else:
        print "Status code other than 200 received!"



def get_user_info(username):
    user_id = get_user_id(username)
    if user_id == None:
        print "This user does not exist!"
        exit()
    request_url = BASE_URL + "users/{id}?access_token={token}".format(id=user_id,token=TOKEN)
    user_info = requests.get(request_url).json()
    # pprint(user_info)
    if user_info['meta']['code'] == 200:
        # print users details
        if 'data' in user_info:
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print "There is no data for this user!!!"
    else:
        print 'Status code other than 200 received!'


def get_own_post():
    END_POINT = 'users/self/media/recent/'
    user_media = requests.get(BASE_URL+END_POINT+ACCESS_TOKEN).json()
    # pprint(user_media)
    if user_media['meta']['code'] == 200:
        #extract post ID
        if len(user_media['data']):
            img_name = user_media['data'][0]['id']+'.jpeg'
            img_url = user_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(img_url,img_name)
            print "Your image has been saved"
        else:
            print "Post doesn't exist"
        # pprint(user_media['data'][0])
    else:
        print "Status code other than 200 received!"

def self_info():
    END_POINT = 'users/self/'
    request_url = (BASE_URL + END_POINT+ACCESS_TOKEN)
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
        get_own_post()
    else:
        print 'Status code other than 200 received!'

# def get_info():
#     #
#     pprint(user_info.json())
# self_info()
# get_user_post('nimitsachdeva')

def start_bot():
    while True:
        print '\n'
        print 'Hey! Welcome to instaBot!'
        print 'Here are your menu options:'
        print "a.Get your own details\n"
        print "b.Get details of a user by username\n"
        print "c.Get your own recent post\n"
        print "d.Get the recent post of a user by username\n"
        print "z.Exit"

        choice = raw_input("Enter you choice: ")
        if choice == "a":
            self_info()
        elif choice == "b":
            insta_username = raw_input("Enter the username of the user: ")
            get_user_info(insta_username)
        elif choice == "c":
            get_own_post()
        elif choice == "d":
            insta_username = raw_input("Enter the username of the user: ")
            get_user_post(insta_username)
        elif choice == "z":
            exit()
        else:
            print "wrong choice"

start_bot()