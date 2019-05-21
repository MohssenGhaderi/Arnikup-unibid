from project import app, redis_db
import json
import time
from rejson import Client, Path

def redis_test():
    rj = Client(host='localhost', port=6379)

    # Set the key `obj` to some object
    obj = {
        'answer': 42,
        'arr': [None, True, 3.14],
        'truth': {
            'coord': 'out there'
        }
    }
    rj.jsonset('obj', Path.rootPath(), obj)

    # Get something
    print ('Is there anybody... {}?'.format(
        rj.jsonget('obj', Path('.truth.coord'))
    ))

    # Delete something (or perhaps nothing), append something and pop it
    rj.jsondel('obj', Path('.arr[0]'))
    rj.jsonarrappend('obj', Path('.arr'), 'something')
    print ('{} popped!'.format(rj.jsonarrpop('obj', Path('.arr'))))

    # Update something else
    rj.jsonset('obj', Path('.answer'), 2.17)

    # And use just like the regular redis-py client
    jp = rj.pipeline()
    jp.set('foo', 'bar')
    jp.jsonset('baz', Path.rootPath(), 'qaz')
    jp.execute()

def redis_set(key,value,expire):
    now = int(time.time())
    expires = now + expire
    p = redis_db.pipeline()
    p.set(key, value)
    p.expireat(key, expire)
    return p.execute()

def redis_modify(key,value,expire):
    now = int(time.time())
    expires = now + expire
    p = redis_db.pipeline()
    p.delete(key)
    p.set(key, value)
    p.expireat(key, expire)
    return p.execute()
