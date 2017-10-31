import requests
from pprint import pprint
import urllib
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

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
            for data_item in user_media['data']:
                media_id = data_item['id']
                media_type = data_item['type']
                media_link = data_item[media_type + 's']['standard_resolution']['url']
                query = Media.select().where(Media.media_id == media_id)
                if len(query) > 0:
                    query[0].media_type = media_type
                    query[0].media_link = media_link
                    query[0].save()
                else:
                    new_media = Media(user_id=user_id, media_id=media_id, media_type=media_type, media_link=media_link)
                    new_media.save()
                    return user_media['data'][0]['id']
                    # img_name = user_media['data'][0]['id']+'.jpeg'
                    # img_url = user_media['data'][0]['images']['standard_resolution']['url']
                    # urllib.urlretrieve(img_url,img_name)
                    #  print "Your image has been saved"
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


def like_a_post(insta_username):
    media_id = get_post_id(insta_username)
    request_url = BASE_URL + 'media/{}/likes'.format(media_id)
    payload = {"access_token": TOKEN}
    post_a_like = requests.post(request_url, payload).json()
    if post_a_like['meta']['code'] == 200:
        print 'Like was successful!'
    else:
        print 'Your like was unsuccessful. Try again!'


def post_a_comment(insta_username):
    media_id = get_post_id(insta_username)
    comment = raw_input("Your comment: ")
    payload = {"access_token": TOKEN, "text" : comment}
    request_url = BASE_URL + 'media/{}/comments'.format(media_id)
    make_comment = requests.post(request_url, payload).json()
    if make_comment['meta']['code'] == 200:
        print "Successfully added a new comment!"
    else:
        print "Unable to add comment. Try again!"


def delete_negative_comment(insta_username):
    media_id = get_post_id(insta_username)
    request_url = BASE_URL + 'media/{}/comments/?access_token={}'.format(media_id,TOKEN)
    # print 'GET request url : %s' % (request_url)
    comment_info = requests.get(request_url).json()
    if comment_info['meta']['code'] == 200:
        if len(comment_info['data']):
            for index in range(0, len(comment_info['data'])):
                comment_id = comment_info['data'][index]['id']
                comment_text = comment_info['data'][index]['text']
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
                if (blob.sentiment.p_neg > blob.sentiment.p_pos):
                    print 'Negative comment : %s' % (comment_text)
                    delete_url = BASE_URL + 'media/{}/comments/{}/?access_token={}'.format(media_id, comment_id, TOKEN)
                    # print 'DELETE request url : %s' % (delete_url)
                    delete_info = requests.delete(delete_url).json()

                    if delete_info['meta']['code'] == 200:
                        print 'Comment successfully deleted!\n'
                    else:
                        print 'Unable to delete comment!'
                else:
                    print 'Positive comment : {}\n'.format(comment_text)
        else:
            print 'There are no existing comments on the post!'
    else:
        print 'Status code other than 200 received!'


def get_like_list(insta_username):
    media_id = get_post_id(insta_username)
    request_url = BASE_URL + 'media/{}/likes?access_token={}'.format(media_id,TOKEN)
    like_info = requests.get(request_url).json()

    if like_info['meta']['code'] == 200:
        if len(like_info['data']) > 0:
            for user_info in like_info['data']:
                print ("Liked by: {}").format(user_info["full_name"])
        else:
            print 'There are no existing comments on the post!'
    else:
        print 'Status code other than 200 received!'


def get_comment_list(insta_username):
    media_id = get_post_id(insta_username)
    request_url = BASE_URL + 'media/{}/comments?access_token={}'.format(media_id, TOKEN)
    comment_info = requests.get(request_url).json()

    if comment_info['meta']['code'] == 200:
        if len(comment_info['data']) > 0:
            for user_info in comment_info['data']:
                comment_text = user_info["text"]
                comment_user = user_info["from"]["full_name"]
                print ("Comment: {} \nAdded by: {}.\n\n").format(comment_text, comment_user)
        else:
            print 'There are no existing comments on the post!'
    else:
        print 'Status code other than 200 received!'


def get_post_id(username):
    id = get_user_id(username)
    if id == None:
        print "This user doesn't exist!"
        exit()
    request_url = BASE_URL + 'users/{user_id}/media/recent/?access_token={token}'.format(user_id=id, token=TOKEN)
    user_media = requests.get(request_url).json()
    if user_media['meta']['code'] == 200:
        if len(user_media['data']) > 0:
            # print user_media['data'][0]['id']
            return user_media['data'][0]['id']
        else:
            print 'There is no recent post of the user!'
            exit()
    else:
        print 'Status code other than 200 received!'
        exit()

def add_user_details(insta_username):
    user_id = get_user_id(insta_username)
    request_url = BASE_URL + 'users/{}/?access_token={}'.format(user_id, TOKEN)
    response = requests.get(request_url).json()
    # print response
    if response['meta']['code'] == 200:
        username = response['data']['username']
        full_name = response['data']['full_name']
        follows = response['data']['counts']['follows']
        followed = response['data']['counts']['followed_by']

        query = User.select().where(User.user_id == user_id)
        if len(query) > 0:
            # then user exist in the database as it will get all the details of the user, we will update it
            query[0].username = username
            query[0].full_name = full_name
            query[0].follows_count = follows
            query[0].followed_by_count = followed
            query[0].save()
        else:
            # user do not exist in the database , we will save it
            new_user = User(user_id=user_id, username=username, full_name=full_name,
                            follows_count=follows, followed_by_count=followed)
            new_user.save()

    else:
        print 'Status code other than 200 received!'
        exit()


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
        print "e.Get a list of people who have liked the recent post of a user\n"
        print "f.Like the recent post of a user\n"
        print "g.Get a list of comments on the recent post of a user\n"
        print "h.Make a comment on the recent post of a user\n"
        print "i.Delete negative comments from the recent post of a user\n"
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
        elif choice == "e":
            insta_username = raw_input("Enter the username of the user: ")
            get_like_list(insta_username)
        elif choice == "f":
            insta_username = raw_input("Enter the username of the user: ")
            like_a_post(insta_username)
        elif choice == "g":
            insta_username = raw_input("Enter the username of the user: ")
            get_comment_list(insta_username)
        elif choice == "h":
            insta_username = raw_input("Enter the username of the user: ")
            post_a_comment(insta_username)
        elif choice == "i":
            insta_username = raw_input("Enter the username of the user: ")
            delete_negative_comment(insta_username)
        elif choice == "z":
            exit()
        else:
            print "wrong choice"

# start_bot()
# like_a_post('nimitsachdeva')
# get_post_id('nimitsachdeva')
# post_a_comment('nimitsachdeva')
# delete_negative_comment('nimitsachdeva')
# get_like_list("nimitsachdeva")
# get_comment_list('nimitsachdeva')