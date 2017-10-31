import peewee
import requests
from main import get_user_id,BASE_URL,TOKEN
from pprint import pprint

database = peewee.SqliteDatabase('user_info.db')

class User(peewee.Model):
    user_id = peewee.CharField(unique=True)
    username = peewee.CharField()
    follows_count = peewee.IntegerField()
    full_name = peewee.CharField()
    followed_by_count = peewee.IntegerField()

    class Meta:
        database = database

class Media(peewee.Model):
    user_id = peewee.ForeignKeyField(User, to_field="user_id")
    media_id = peewee.CharField(unique=True)
    media_type = peewee.CharField()
    media_link = peewee.CharField()

    class Meta:
        database = database

class Comment(peewee.Model):
    comment_id = peewee.CharField(unique=True)
    media_id = peewee.ForeignKeyField(Media, to_field="media_id")
    user_id = peewee.ForeignKeyField(User, to_field="user_id")
    comment_text = peewee.CharField()

    class Meta:
        database = database

def initialize_db():
    database.create_tables([User, Media, Comment], safe=True)

initialize_db()


def add_comments(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = BASE_URL + 'users/{}/media/recent/?access_token={}'.format(user_id, TOKEN)
    user_media = requests.get(request_url).json()
    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            for index in range(len(user_media['data'])):
                media_id = user_media['data'][index]['id']
                print media_id
                comment_request = BASE_URL + 'media/{}/comments?access_token={}'.format(media_id, TOKEN)
                # print 'GET request url :{}'.format(comment_request)
                response = requests.get(comment_request).json()
                if response['meta']['code'] == 200:
                    for index in range(len(response['data'])):
                        # pprint(response['data'])
                        #Retrieve Comment Details
                        #Add to Database

add_comments('nimitsachdeva')
# add_user_details('nimitsachdeva')

# new_user = User(user_id=5, username="eeshani_p",full_name="Eeshani Patel", follows_count=200,followed_by_count=300)
# new_user.save()
# print new_user.username