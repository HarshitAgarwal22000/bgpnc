from fastapi import FastAPI,HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
import jwt
import subprocess
import os
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
    query='select token_id from token_jwt where (token_id = ? && valid="1")'
    cursor.execute(query,(token,))
    fetchToken= cursor.fetchone()[0]
    print("Token",fetchToken)
    dect=jwt.decode(token, SECRET_KEY, algorithms="HS256")
    db=jwt.decode(fetchToken, SECRET_KEY, algorithms='HS256')
    if(db==dect):
        return True
    else:
        return False
        


SECRET_KEY=os.urandom(32)
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
        'Asn':datas['Asn'],
    

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
        returnDat={
            "Auth":token,
            "Message":"SIgned in Succesfully"
        }
        return(returnDat)
    except mariadb.Error as error:
    
        print(error)
        return({"Message":"Failed"})
@app.get('/interfaces/{router_id}')
async def get_interfaces(router_id:str, authorization : str= Header(...)):
    if(check_token(router_id, authorization)):
          result = subprocess.run(["sudo", "vtysh", "-c", 'show interface'], capture_output=True, text=True, check=True)
          return ({"message":f"{result.stdout}"})
    else:
        return ({"message":"Not valid"})
 
    
    return{"get":"dara"}
@app.post('/neighbors/{router_id}')
async def neighbors(router_id:str, authorization : str=Header(...)):
    if(check_token(router_id,authorization)):
        result=subprocess.run(['sudo','vtysh','-c',"show bgp neighbors"], capture_output=True, text=True, check=True)
        print(result.stdout)
    
    return ({"message":f"{result.stdout}"})
@app.post('/bgp/{router_id}')
async def bgp(router_id:str, authorization: str=Header(...)):
    if(check_token(router_id, authorization)):
        result=subprocess.run(['sudo','vtysh','-c',"show ip bgp summary"], capture_output=True, text=True, check=True)
        print(result.stdout)
        return({"message":f"{result.stdout}"})
    else:
        print("Error")
    
@app.post('/logout')
async def logout(data: dict):
    con=mariadb.connect(**db_con)
    print(data)
    cursor=con.cursor()
    token=data['Token']
    stat='UPDATE token_jwt SET valid="0" WHERE token_id = ?'
    par=[token]
    cursor.execute(stat,par)
    con.commit()
    return({"message":"API hit"})


