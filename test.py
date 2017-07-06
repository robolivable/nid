import itertools
import nnid
import random
import string
import time

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
            t_s = nnid.generate(s)
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
            t_s = nnid.generate(s)
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

