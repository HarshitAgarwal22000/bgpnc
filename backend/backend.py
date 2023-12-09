from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware
import jwt
import mariadb

from fastapi.encoders import jsonable_encoder

app=FastAPI()


db_con={
    "username":"harshit",
    "host":"localhost",
    "password":"123",
    "database":"sv"
}
def check_token(rid,token):
    conn=mariadb.connect(**db_con)
    cursor=conn.cursor()
    query='select token from login_users where routerid = ?'
    cursor.execute(query,(rid,))
    fetchToken=cursor.fetchone()
    sig=token.split('.')
    fetchSignature=fetchToken[0].split('.')
    if(sig[2]==fetchSignature[2]):
        return True
    else:
        return False

    print("sigNATURE",sig[2])
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
SECRET_KEY="DUBAI"
@app.get('/')
def home():
    return ({"darab":"dinsid"})
@app.post('/login')
def login(data : dict):
    recd=jsonable_encoder(data)
    rid=(recd['cred']['RouterID'])
    passw=recd['cred']['enPass']
    con=mariadb.connect(**db_con)
    cursor=con.cursor()
    print(rid)
    t='select * from login_users where routerid =?'
    cursor.execute(t,(rid,))
    if(cursor.fetchone()):
        print("Username found")
        st='select * from login_users where password=?'
        cursor.execute(st,(passw,))
        if(cursor.fetchone()):
            print("Password validated")
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
        

      
    payload={
        "exp":1701924522,
        "Success":True,
        "User":"Validated"
    }
    
    token=jwt.encode(payload,SECRET_KEY,algorithm="HS256")
    json_data=({
        "Auth":token
    })
    print(token)
    return (json_data)
@app.post('/signup/{router_id}')
async def sign(router_id : str, data: dict):


    con=mariadb.connect(**db_con)
    cursor=con.cursor()
    datas=jsonable_encoder(data)
    print(datas)
    print(router_id)
    payload={
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
        return({"Message":"Signed In Successfully"})
    except mariadb.Error as error:
    
        print(error)
        return({"Message":"Failed"})
    

