import requests,json,sqlite3
def wget(UA,url,uid):
    try:
        cache=requests.get(url,headers=UA,timeout=5)
        cache.raise_for_status()
        cache.encoding=cache.apparent_encoding
        return cache.text
    except:
        print("[DEBUG]:Failed to fetch uid %d."%uid)
        print(cache.status_code)
        return ""
def parse(stdin,uid):
    try:
        parsed=json.loads(stdin)
        return parsed
    except:
        print("[DEBUG]:Failed to parse the information of uid %d"%uid)
        return ""
def splitdata(stdin,uid):
    try:
        var=stdin['Variables']
        inf=var['space']
        #TODO: Export information.
        uid=int(inf['uid'])
        username=inf['username']
        emailstatus=int(inf['emailstatus'])
        avatarstatus=int(inf['avatarstatus'])
        group=inf['group']
        groupid=group['grouptitle']
        extgroupids=inf['extgroupids']
        credits=int(inf['credits'])
        extcredits1=int(inf['extcredits1'])
        extcredits2=int(inf['extcredits2'])
        extcredits3=int(inf['extcredits3'])
        extcredits4=int(inf['extcredits4'])
        extcredits8=int(inf['extcredits8'])
        friends=int(inf['friends'])
        posts=int(inf['posts'])
        threads=int(inf['threads'])
        replys=int(posts)-int(threads)
        digestposts=int(inf['digestposts'])
        views=int(inf['views'])
        oltime=int(inf['oltime'])
        follower=int(inf['follower'])
        following=int(inf['following'])
        blacklist=int(inf['blacklist'])
        medals=len(inf['medals'])
        lastvisit=inf['lastvisit']
        gender=int(inf['gender'])
        return (uid,username,credits,extcredits1,extcredits2,extcredits3,extcredits4,extcredits8,medals,digestposts,blacklist,oltime,replys,threads,posts,friends,follower,following,views,groupid,extgroupids,lastvisit,gender,emailstatus,avatarstatus)
    except:
        print("[DEBUG]:Failed to spilt the information of uid %d"%uid)
        return ""
def dbprocess(uid,*args):
    db=sqlite3.connect("userdata.sqlite3")
    c=db.cursor()        
    c.execute("CREATE TABLE IF NOT EXISTS users(uid INT NOT NULL PRIMARY KEY, username CHAR(100) NOT NULL, credits INT NOT NULL, extcredits1 INT NOT NULL, extcredits2 INT NOT NULL, extcredits3 INT NOT NULL, extcredits4 INT NOT NULL, extcredits8 INT NOT NULL, medals INT NOT NULL, digestposts INT NOT NULL, blacklist INT NOT NULL, oltime INT NOT NULL, replys INT NOT NULL, threads INT NOT NULL, posts INT NOT NULL, friends INT NOT NULL, follower INT NOT NULL, following INT NOT NULL, views INT NOT NULL, groupid CHAR(100) NOT NULL, extgroupids CHAR(100), lastvisit CHAR(100) NOT NULL, gender INT, emailstatus INT NOT NULL, avatarstatus INT NOT NULL);")
    try:
        for i in args:
            print(i)
            c.execute("INSERT INTO users VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10],i[11],i[12],i[13],i[14],i[15],i[16],i[17],i[18],i[19],i[20],i[21],i[22],i[23],i[24]))
        db.commit()
        db.close()
        return
    except:
        print("[DEBUG]:Failed to write data into database of uid %d."%uid)
        db.close()
        return
def fetch(uid):
    url="https://*/api/mobile/index.php?version=4&module=profile&uid=%d"%uid
    UA={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15"}
    origin=wget(UA,url,uid)
    parsed=parse(origin,uid)
    processed=splitdata(parsed,uid)
    dbprocess(uid,processed)
def main():
    for i in range(*,*):
        fetch(i)

main()
