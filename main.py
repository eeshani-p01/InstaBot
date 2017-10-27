import requests

response = requests.get('https://jsonbin.io/b/906cb6c4edd44c9988e9c253448f1b82').json()
APP_ACCESS_TOKEN = response['access_token']


def self_info():
    request_url = (BASE_URL + 'users/self/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
    # print users details

    else:
        print 'Status code other than 200 received!'