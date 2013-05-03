from urllib2 import urlopen
from json import loads

from data import data

SIMULATE_TWITTER = True

class FakeTwitter(object):
    def PostUpdate(self, msg, **kwargs):
        with open('twitter.out', 'w') as outfile:
            outfile.write(msg)
            
if not SIMULATE_TWITTER:
    from twitter import Api
    
    twitter = Api(consumer_key = data.twitter_consumer_key,
                   consumer_secret = data.twitter_consumer_secret,
                   access_token_key = data.twitter_access_token,
                   access_token_secret = data.twitter_access_token_secret)
else:
    twitter = FakeTwitter()

def twitter_post(msg):
    twitter.PostUpdate(msg,
                       latitude = data.last_latitude,
                       longitude = data.last_longitude) 
    
def get_beverage_description(upc):
    
    upc = int(upc)
    
    beverage = data.get_beverage(upc)
    if beverage: return beverage.description
    
    url = ('http://www.upcdatabase.org/api/json/%s/%0.12d/' %
           (data.upc_database_key, upc))
    resp = urlopen(url)
    jsondata = resp.read()
    upcdata = loads(jsondata)
    
    if upcdata['valid'] == 'true':
        description = upcdata['description']
        try:
            data.new_beverage(upc, description)
        finally:
            return description
    else:
        return None
    
def get_user():
    
    return None

def update_user(user_id):

    data.update_user(user_id)
    
def log(upc):
    data.log(upc)