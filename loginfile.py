from fastapi import FastAPI , HTTPException , Path , Query 
from pydantic import BaseModel , Field , EmailStr , field_validator
from typing import Annotated , List , Dict
from fastapi.responses import JSONResponse
import json
from pwhashed import hash_password , verify_password


app = FastAPI()

class login_details(BaseModel):
    email : EmailStr
    password : Annotated[str , Field(..., description="Passowrd must be with in 0-12 characters")]
    
    #Email Validating
    @field_validator('email' , mode='after')
    @classmethod
    def email_validate(cls , value):
        valid_domain = ['gmail.com']
        #email split 
        domain = value.split('@')[-1]
        if domain  not in valid_domain:
            raise ValueError("Not Valid Domain use '@gmail.com'")
        return value  #should be return if all check
    
def read_file():
    with open("login.json" , "r") as f:
        data = json.load(f)
        return data 
def write_file(data):
    with open("login.json" , "w") as f:
        json.dump(data , f)


@app.get("/about")
def aboutweb():
    return {"Authentication System" : "Email & Password"}

@app.post("/account")
def account_check(user : login_details):
    data = read_file()
    for acc in data["users"]:
        if user.email == acc["email"]:
            #Veeify hash password
            if verify_password(user.password, acc["password"]):
                return acc
            raise HTTPException(status_code=401 , detail="Wrong password")
    raise HTTPException(status_code=401 , detail="Invalid Account details")

@app.post("/create")
def create_account(account : login_details):
    data = read_file()
    for acc in data["users"]:
        if account.email == acc["email"]:
            raise HTTPException(status_code=401 , detail="Already present")
    
    new_account = account.model_dump()
    #Hashing password
    new_account["password"] = hash_password(account.password)
    
    data["users"].append(new_account)
    write_file(data)
    return JSONResponse(status_code=200 , content={"account created" : "Successfull created"})