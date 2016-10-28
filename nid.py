# Namespace ID for NoSQL
# Generate a 64 bit Namespace ID. Used for generating pseudo random IDs for 
# users.
#
# This algorithm is based on the time since a predefined EPOCH date, and
# two factors of randomness:
#    1. Lexical product value of username mod 2**16 (to fit into 16 bits)
#    2. A pseudo random number from 0 to 2**8-1
#
# This can guarentee uniqueness up to 99.9999% as long as it isn't used to
# generate more than 40 IDs per millisecond.

import itertools
import random
import string
import time

EPOCH = 1412740800000
ASCII_FREQ_TABLE = {
        'e':1,'a':2,'o':3,'i':4,'r':5,'n':6,'s':7,'t':8,
        'l':9,'d':10,'b':11,'m':12,'u':13,'k':14,'g':15,
        'h':16,'c':17,'y':18,'p':19,'f':20,'j':21,'v':22,
        'w':23,'z':24,'1':25,'2':26,'0':27,'6':28,'3':29,
        '8':30,'4':31,'7':32,'5':33,'9':34,'x':35,'_':36,
        'q':37,'-':38
    } # based on character use frequency
ASCII_TABLE = {
        'a':1,'b':2,'c':3,'d':4,'e':5,'f':6,'g':7,'h':8,
        'i':9,'j':10,'k':11,'l':12,'m':13,'n':14,'o':15,
        'p':16,'q':17,'r':18,'s':19,'t':20,'u':21,'v':22,
        'w':23,'x':24,'y':25,'z':26,'0':27,'1':28,'2':29,
        '3':30,'4':31,'5':32,'6':33,'7':34,'8':35,'9':36,
        '-':37,'_':38
    }
ASCII_HEX_FREQ_TABLE_PRIME = {
        'e':0x02,'a':0x03,'o':0x05,'i':0x07,'r':0x0b,'n':0x0d,'s':0x11,
        't':0x13,'l':0x17,'d':0x1d,'b':0x1f,'m':0x25,'u':0x29,'k':0x2b,
        'g':0x2f,'h':0x35,'c':0x3b,'y':0x3d,'p':0x43,'f':0x47,'j':0x49,
        'v':0x4f,'w':0x53,'z':0x59,'1':0x61,'2':0x65,'0':0x67,'6':0x6b,
        '3':0x6d,'8':0x71,'4':0x7f,'7':0x83,'5':0x89,'9':0x8b,'x':0x95,
        '_':0x97,'q':0x9d,'-':0xa3
    } # based on character use frequency

def _n_power(x, n):
    i = 1
    y = 0
    while i < n:
        y = y + x**i
        i += 1
    return y

def _string_lex_cardinal(s, T=ASCII_TABLE, m=2**128):
    h = 0
    h = _n_power(len(T), len(s))
    i = 0
    while i < len(s):
        h += (T[s[i]]-1) * len(T)**int(len(s)-1-i)
        i += 1
    return (h + 1) % m

def generate(s, et=EPOCH):
    """Generate numerical namespace ID for a given string.
    @param s: string to generate from
    @param et: epoch time to base ID from (default is Oct. 08, 2014)
    """
    t = int(round(time.time() * 1000)) - et
    h = t << (64-41)
    h |= _string_lex_cardinal(s, ASCII_FREQ_TABLE, 2**16) << (64-41-15)
    h |= random.randrange(0, (2**8)-1)
    return h

def test_random_collision(limit, s_per_id):
    if not limit:
        raise "limit must be specified"
    try:
        limit = int(limit)
    except:
        raise "invalid limit"

    t_map = {}
    i = 0
    collisions = 0
    stime = int(round(time.time() * 1000))
    r_string_lower = string.lowercase+'_-'
    if s_per_id > 0: # save call to time if s == 0
        for n in range(0, limit):
            s = ''.join(random.choice(r_string_lower) \
                        for x in range(random.randrange(2,16)))
            t_s = generate(s)
            try:
                t_map[t_s]
                collisions += 1
                continue
            except KeyError:
                pass
            t_map[t_s] = s
            time.sleep(s_per_id)
            i += 1
    else:    
        for n in range(0, limit):
            s = ''.join(random.choice(r_string_lower) \
                        for x in range(random.randrange(2,16)))
            t_s = generate(s)
            try:
                t_map[t_s]
                collisions += 1
                continue
            except KeyError:
                pass
            t_map[t_s] = s
            i += 1
    t_time = int(round(time.time() * 1000)) - stime
    print "IDs per millisecond:", float(i) / float(t_time)
    print "Collisions:", collisions

def test_collision(limit, l, m):
    if not limit:
        raise "limit must be specified"
    try:
        limit = int(limit)
    except:
        raise "invalid limit"
    t_map = {}
    i = 0
    for s in itertools.imap(''.join,
             itertools.product('abcdefghijklmnopqrstuvwxyz0123456789-_',
                 repeat=l)):
        if i == limit:
            print "no collisions found within limit of", limit
            return
        t_i = _string_lex_cardinal(s, ASCII_FREQ_TABLE, m)
        try:
            t_map[t_i]
            print "collision:", s, ",", t_i, "with", t_map[t_i]
            return
        except KeyError:
            pass
        t_map[t_i] = s
        i += 1
    print "no collisions found within limit of", limit

