import requests,json,pymysql


def wget(UA, url, uid):
    try:
        cache = requests.get(url, headers=UA, timeout=5)
        cache.raise_for_status()
        cache.encoding = cache.apparent_encoding
        return cache.text
    except:
        print("[DEBUG]:Failed to fetch uid %d." % uid)
        return ""
        
        
def parse(xx, uid):
    try:
        parsed = json.loads(xx)
        return parsed
    except:
        print("[DEBUG]:Failed to parse the information of uid %d" % uid)
        return ""


def splitdata(stdin, uid):
    try:
        var = stdin['Variables']
        inf = var['space']
        uid = inf['uid']
        username = inf['username']
        emailstatus = int(inf['emailstatus'])
        avatarstatus = int(inf['avatarstatus'])
        group = inf['group']
        groupid = group['grouptitle']
        extgroupids = inf['extgroupids']
        cr = int(inf['credits'])
        extcredits1 = int(inf['extcredits1'])
        extcredits2 = int(inf['extcredits2'])
        extcredits3 = int(inf['extcredits3'])
        extcredits4 = int(inf['extcredits4'])
        extcredits8 = int(inf['extcredits8'])
        friends = int(inf['friends'])
        posts = int(inf['posts'])
        threads = int(inf['threads'])
        replys = int(posts)-int(threads)
        digestposts = int(inf['digestposts'])
        views = int(inf['views'])
        oltime = int(inf['oltime'])
        follower = int(inf['follower'])
        following = int(inf['following'])
        blacklist = int(inf['blacklist'])
        medals = len(inf['medals'])
        lastvisit = inf['lastvisit']
        gender = int(inf['gender'])
        return [uid, username, cr, extcredits1, extcredits2, extcredits3,
                extcredits4, extcredits8, medals, digestposts, blacklist,
                oltime, replys, threads, posts, friends, follower, following,
                views, groupid, extgroupids, lastvisit, gender, emailstatus, avatarstatus]
    except:
        print("[DEBUG]:Failed to spilt the information of uid %s" % uid)
        return ""
    
    
def dbprocess(c, db, uid, args):
    try:
        c.execute(
            "INSERT INTO users VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);", args)
        db.commit()
        return
    except:
        print("[DEBUG]:Failed to write data into database of uid %d." % uid)
        return
        

def fetch(c, db, uid):
    url = "https://*/api/mobile/index.php?version=4&module=profile&uid=%d" % uid
    UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15"}
    origin = wget(UA, url, uid)
    parsed = parse(origin, uid)
    processed = splitdata(parsed, uid)
    dbprocess(c, db, uid, processed)
    
    
def main():
    db = pymysql.connect(host='127.0.0.1', user='root', password='***', database='***')
    c = db.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        uid         CHAR(32)     PRIMARY KEY NOT NULL,
        username    VARCHAR(64)  NOT NULL,
        credits     INTEGER      NOT NULL,
        extcredits1 INTEGER      NOT NULL,
        extcredits2 INTEGER      NOT NULL,
        extcredits3 INTEGER      NOT NULL,
        extcredits4 INTEGER      NOT NULL,
        extcredits8 INTEGER      NOT NULL,
        medals      TINYINT      NOT NULL,
        digestposts INTEGER      NOT NULL,
        blacklist   INTEGER      NOT NULL,
        oltime      INTEGER      NOT NULL,
        replys      INTEGER      NOT NULL,
        threads     INTEGER      NOT NULL,
        posts       INTEGER      NOT NULL,
        friends     INTEGER      NOT NULL,
        follower    INTEGER      NOT NULL,
        following   INTEGER      NOT NULL,
        views       INTEGER      NOT NULL,
        groupid     VARCHAR(64)  NOT NULL,
        extgroupids VARCHAR(64)  NOT NULL,
        lastvisit   VARCHAR(32)  NOT NULL,
        gender      TINYINT      NOT NULL,
        emailstatus TINYINT      NOT NULL,
        avatarstatus TINYINT     NOT NULL
    );
    """)
    for i in range(*,*):
        fetch(c,db,i)
    db.close()


main()
