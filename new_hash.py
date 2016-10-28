import itertools
import random
import time

class cardinal_id:
    ASCII_HEX_FREQ_TABLE = {
            'e':'1','a':'2','o':'3','i':'4','r':'5','n':'6','s':'7','t':'8',
            'l':'9','d':'10','b':'11','m':'12','u':'13','k':'14','g':'15',
            'h':'16','c':'17','y':'18','p':'19','f':'20','j':'21','v':'22',
            'w':'23','z':'24','1':'25','2':'26','0':'27','6':'28','3':'29',
            '8':'30','4':'31','7':'32','5':'33','9':'34','x':'35','_':'36',
            'q':'37','-':'38'} # based on character use frequency
    ASCII_HEX_FREQ_TABLE_PRIME = {
            'e':'02','a':'03','o':'05','i':'07','r':'0b','n':'0d','s':'11',
            't':'13','l':'17','d':'1d','b':'1f','m':'25','u':'29','k':'2b',
            'g':'2f','h':'35','c':'3b','y':'3d','p':'43','f':'47','j':'49',
            'v':'4f','w':'53','z':'59','1':'61','2':'65','0':'67','6':'6b',
            '3':'6d','8':'71','4':'7f','7':'83','5':'89','9':'8b','x':'95',
            '_':'97','q':'9d','-':'a3'} # based on character use frequency
    ASCII_HEX_TABLE = {
            'a':'1','b':'2','c':'3','d':'4','e':'5','f':'6','g':'7','h':'8',
            'i':'9','j':'10','k':'11','l':'12','m':'13','n':'14','o':'15',
            'p':'16','q':'17','r':'18','s':'19','t':'20','u':'21','v':'22',
            'w':'23','x':'24','y':'25','z':'26','0':'27','1':'28','2':'29',
            '3':'30','4':'31','5':'32','6':'33','7':'34','8':'35','9':'36',
            '-':'37','_':'38'}
 
    @staticmethod
    def _n_power(x, n):
        i = 1
        y = 0
        while i < n:
            y = y + x**i
            i = i + 1
        return y

    @staticmethod
    def _calculate_string(s, T=ASCII_HEX_TABLE, m=2**16):
        h = 0
        h = cardinal_id._n_power(len(T), len(s))
        i = 0
        while i < len(s):
            h += (int(T[s[i]])-1) * len(T)**int(len(s)-1-i)
            i += 1
        return (h + 1) % m

    def generate_time_id(self, s, t=0):
        if t == 0: t = int(round(time.time() * 1000)) - 1412740800000
        h = t << (64-41)
        h |= cardinal_id._calculate_string(s, cardinal_id.ASCII_HEX_FREQ_TABLE) << (64-41-15)
        h |= random.randrange(0, (2**8)-1)
        return h

    def test_random_collision(self, limit):
        if not limit:
            raise "limit must be specified"
        try:
            limit = int(limit)
        except:
            raise "invalid limit"
        t_map = {}
        for n in range(0, limit):
            s = ''.join(random.choice(string.lowercase) for x in range(randrange(2,16)))
            t_s = self.generate_time_id(s)
            print t_s
            try:
                t_map[t_s]
                print "collision:", s, ",", t_s, "with", t_map[t_s]
                return
            except KeyError:
                pass
            t_map[t_s] = s
        print "no collisions found within limit of", limit



    def test_collision(self, limit, l, m):
        if not limit:
            raise "limit must be specified"
        try:
            limit = int(limit)
        except:
            raise "invalid limit"
        t_map = {}
        i = 0
        for s in itertools.imap(''.join, itertools.product('abcdefghijklmnopqrstuvwxyz0123456789-_', repeat=l)):
            if i == limit:
                print "no collisions found within limit of", limit
                return
            t_i = self._calculate_string(s, cardinal_id.ASCII_HEX_FREQ_TABLE, m)
            try:
                t_map[t_i]
                print "collision:", s, ",", t_i, "with", t_map[t_i]
                return
            except KeyError:
                pass
            t_map[t_i] = s
            i += 1
        print "no collisions found within limit of", limit

# OLD
#        USERNAME = sys.argv[1]
#        un_hash = 0
#        un_hash = f_power(38, len(USERNAME)) 
#        #print "f_power(38,", len(USERNAME)-1, ")=", un_hash
#        i = 0
#        while i < len(USERNAME):
#            #un_hash = un_hash + (38**int(len(USERNAME)-(i+1)))*int(ASCII_HEX_FREQ_TABLE[USERNAME[i]], 16)
#
#            #print 38, "**", int(len(USERNAME)-(i+1)), "*", int(ASCII_HEX_TABLE[USERNAME[i]]), "=", (38**int(len(USERNAME)-(i+1)))*int(ASCII_HEX_TABLE[USERNAME[i]])
#            #un_hash = un_hash + (38**int(len(USERNAME)-(i+1)))*int(ASCII_HEX_TABLE[USERNAME[i]])
#
#            #un_hash += (int(ASCII_HEX_TABLE[USERNAME[i]])**int(len(USERNAME)-(i)))
#
#            un_hash += (int(ASCII_HEX_TABLE[USERNAME[i]])-1) * 38**int(len(USERNAME)-1-i)
#            #print (int(ASCII_HEX_TABLE[USERNAME[i]])-1), "*", "38 to power of", int(len(USERNAME)-1-i), "=", un_hash
#            i = i + 1
#
#        un_hash += 1
#        print un_hash % (2**16)


