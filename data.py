import sqlite3

TWITTER_CONSUMER_KEY = 'twitter_consumer_key'
TWITTER_CONSUMER_SECRET = 'twitter_consumer_secret'
TWITTER_ACCESS_TOKEN = 'twitter_access_token'
TWITTER_ACCESS_TOKEN_SECRET = 'twitter_access_token_secret'
LAST_LATITUDE = 'last_latitude'
LAST_LONGITUDE = 'last_longitude'
UPC_DATABASE_KEY = 'upc_database_key'

USER_TIMEOUT = 500

class Data(object):

    conn = sqlite3.connect('CoD.db')
    c = conn.cursor()
    
    def __del__(self):
        self.conn.commit()
        self.c.close()
        self.conn.close()
    
    def _getter(self, key):
        self.c.execute('SELECT value FROM kvs WHERE key=?', (key,))
        out = self.c.fetchone()[0]
        return out
    
    @property
    def last_latitude(self): return self._getter(LAST_LATITUDE)
    
    @property
    def last_longitude(self): return self._getter(LAST_LONGITUDE)
    
    @property
    def twitter_access_token(self): return self._getter(TWITTER_ACCESS_TOKEN)
    
    @property
    def twitter_access_token_secret(self):
        return self._getter(TWITTER_ACCESS_TOKEN_SECRET)
    
    @property
    def twitter_consumer_key(self):
        return self._getter(TWITTER_CONSUMER_KEY)
    
    @property
    def twitter_consumer_secret(self):
        return self._getter(TWITTER_CONSUMER_SECRET)
    
    @property
    def upc_database_key(self):
        return self._getter(UPC_DATABASE_KEY)
    
    def get_beverage(self, upc):
        self.c.execute('SELECT upc, description, untappd_id FROM beverages WHERE upc = ?',
                       (upc,))
        ret = self.c.fetchone()
        return Beverage(ret) if ret else None
    
    def new_beverage(self, upc, description):
        self.c.execute('''INSERT
                          INTO beverages (upc, description, untappd_id)
                          VALUES (?, ?, ?)''',
                          (upc, description, ''))
        self.conn.commit()
        
    def update_user(self, user_id):
        print 'updating user ', user_id
        self.c.execute('''UPDATE users
                          SET last_seen=datetime('now')
                          WHERE user_id=?''',
                          (user_id,))
        
    def log(self, upc):
        self.c.execute('''INSERT INTO log(upc, timestamp)
                          VALUES (?, datetime('now'))''',
                          (upc,))
        
    def get_current_user(self):
        self.c.execute('''SELECT *
                          FROM users 
                          WHERE last_seen BETWEEN datetime('now','-500 seconds')
                          AND datetime('now')
                          ORDER BY last_seen DESC
                          LIMIT 1
                          ''')
        
        ret = self.c.fetchone()
        if ret is not None: return User(ret)
        
    def log_beverage(self, user, beverage):
        self.c.execute('''INSERT
                          INTO drinks(user_id, beverage_id, timestamp)
                          VALUES (?, ?, datetime('now'))''',
                          (user.id, beverage.upc))
        
class Beverage(object):
    def __init__(self, tup):
        if type(tup) is tuple:
            self.upc, self.description, self.untapped_id = tup
            
class User(object):
    def __init__(self, tup):
        if type(tup) is tuple:
            self.user_id, self.name, self.email, self.last_seen, self.twitter_handle = tup
    
data = Data()