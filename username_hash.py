import itertools
import sys

ASCII_HEX_FREQ_TABLE = { # based on character use frequency
            'e':'02',
            'a':'03',
            'o':'05',
            'i':'07',
            'r':'0b',
            'n':'0d',
            's':'11',
            't':'13',
            'l':'17',
            'd':'1d',
            'b':'1f',
            'm':'25',
            'u':'29',
            'k':'2b',
            'g':'2f',
            'h':'35',
            'c':'3b',
            'y':'3d',
            'p':'43',
            'f':'47',
            'j':'49',
            'v':'4f',
            'w':'53',
            'z':'59',
            '1':'61',
            '2':'65',
            '0':'67',
            '6':'6b',
            '3':'6d',
            '8':'71',
            '4':'7f',
            '7':'83',
            '5':'89',
            '9':'8b',
            'x':'95',
            '_':'97',
            'q':'9d',
            '-':'a3'
        }
    
class username_hash():
    def __init__(self):
        pass

    def f_x(self, p, ch, n):
        t_ch = '0x'
        for c in ch:
            t_ch += ASCII_HEX_FREQ_TABLE[c]
        p += int(t_ch, 16)
        try:
            p += (int(ASCII_HEX_FREQ_TABLE[ch[0]], 16)**n)*31
        except IndexError:
            pass
        try:
            p += (int(ASCII_HEX_FREQ_TABLE[ch[1]], 16)**n)*31 
        except IndexError:
            pass
        try:
            p += (int(ASCII_HEX_FREQ_TABLE[ch[2]], 16)**n)*31
        except IndexError:
            pass
        return p

    def f_x2(self, p, c, n):
        p += 31*p+ord(c)
        return p

    def un_hash(self, arg):
        if not isinstance(arg, basestring):
            raise 'cannot generate hash'
        arg = arg.lower()
        user_id = 0
        #for s in range(0, len(arg), 3):
            #user_id = self.f_x(user_id, arg[s:s+3], (s/3)+1)
        #    user_id = self.f_x(user_id, arg[s:s+3], (len(arg)-((s/3)+1)))
#        for i, s in enumerate(arg):
#            user_id = self.f_x2(user_id, s, len(arg)-i)
#        for s in arg:
#            user_id = 31*user_id+ord(s)
        t_ch = '0x'
        for c in arg:
            t_ch += ASCII_HEX_FREQ_TABLE[c]
        user_id += int(t_ch, 16)
        return user_id

    def test_collision(self, limit, r):
        if not limit:
            raise "limit must be specified"
        try:
            limit = int(limit)
        except:
            raise "invalid limit"
        t_map = {}
        i = 0
        for s in itertools.imap(''.join, itertools.product('abcdefghijklmnopqrstuvwxyz0123456789-_', repeat=r)):
            if i == limit:
                print "no collisions found within limit of", limit
                return
            t_i = self.un_hash(s)
            try:
                t_map[t_i]
                print "collision:", s, ",", t_i, "with", t_map[t_i]
                break;
            except KeyError:
                pass
            t_map[t_i] = s
            i += 1

        

