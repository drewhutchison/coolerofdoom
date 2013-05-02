from sys import argv, exit

import functions as f

if len(argv) != 2:
    print 'usage: %s <upc>' % argv[0]
    exit(-1)
    
upc = argv[1]

f.log(upc)

if upc[0] == '4':
    
    if upc[6] == '1':
        
        f.update_user(int(upc[-5:-1]))
        
elif upc[0] in [str(i) for i in [0,1,6,7,8]]:
    
    user = f.get_user()
    username = ((user.twitter_handle if user.twitter_handle
                 else user.name) if user
                else 'Somebody')
    beveragename = f.get_beverage_description(upc)
    print 'beveragename: ', beveragename
    if not beveragename: beveragename = 'something'
    
    f.twitter_post('%s grabbed a %s' % (username, beveragename))
    
else:
    
    print 'don\'t know what that is'