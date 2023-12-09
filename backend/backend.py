from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware
import jwt
import time
import mariadb

from fastapi.encoders import jsonable_encoder

app=FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db_con={
    "username":"harshit",
    "host":"localhost",
    "password":"123",
    "database":"sv"
}
def check_token(rid,token):
    conn=mariadb.connect(**db_con)
    cursor=conn.cursor()
    query='select * from token_jwt where token_id = ?'
    cursor.execute(query,(rid,))
    fetchToken=cursor.fetchone()
    sig=token.split('.')
    fetchSignature=fetchToken[0].split('.')
    if(sig[2]==fetchSignature[2]):
        dect=jwt.decode(token)
        if(dect['exp']<time.time()):
            return jwt.ExpiredSignatureError
        else:


            return True
    else:
        return False


SECRET_KEY="DUBAI"
@app.get('/')
def home():
    return ({"darab":"dinsid"})
@app.post('/login')
def login(data : dict):
    print("Server")
    recd=jsonable_encoder(data)
    rid=(recd['cred']['RouterID'])
    passw=recd['cred']['enPass']
    con=mariadb.connect(**db_con)
    cursor=con.cursor()
    print(rid)
    t='select * from login_users where routerid =?'
    cursor.execute(t,(rid,))
    if(cursor.fetchall()):
        print("Username found")
        st='select * from login_users where password=?'
        cursor.execute(st,(passw,))
        if(cursor.fetchone()):
            print("Password validated")
            payload={
        "exp":int(time.time())+86400,
        "iat":int(time.time()),
        "Success":True,
        "User":"Validated",
        "Username":rid,
    }
            print(payload['exp'])
            token=jwt.encode(payload,SECRET_KEY,algorithm="HS256")
            sta='insert into token_jwt (token_id, exp, iat , valid) values (?, ?, ?, ?)'
            dat=[token, payload['exp'], payload['iat'], "1"]
            cursor.execute(sta,dat)
            con.commit()

            
            json_data=({
                "Auth":token
            })
            print(token)
            return (json_data)
        else:
            print("INvalid ")
            raise HTTPException(
                status_code=401,
                detail="Invalid credential"
            )
    else:
        print("Invalid")
        raise HTTPException(
                status_code=401,
                detail="Invalid credential"
            )
        

      
   
@app.post('/signup/{router_id}')
async def sign(router_id : str, data: dict):


    con=mariadb.connect(**db_con)
    cursor=con.cursor()
    datas=jsonable_encoder(data)
    print(datas)
    print(router_id)
    expt=int(time.time())+86400
    payload={
        "exp":expt,
        "iat":int(time.time()),
        "rid":router_id,
        'password':datas['Password'],
        'Asn':datas['Asn']

    }
 
    token=jwt.encode(payload,SECRET_KEY,'HS256')
    query="insert into login_users (routerid, password, asn, token) values (?, ?, ?, ?);"
    data=[router_id, datas['Password'], datas['Asn'], token]
    print(data)
    try:
        cursor.execute(query,data)
        con.commit()
        sta='insert into token_jwt (token_id, exp, iat, valid) values ? ? ? ?'
        d=[token, payload['exp'], payload['iat'], "1"]
        cursor.execute(sta,d)
        con.commit()
        return({"Message":"Signed In Successfully"})
    except mariadb.Error as error:
    
        print(error)
        return({"Message":"Failed"})
    

