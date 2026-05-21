from fastapi import FastAPI , HTTPException , Path , Query 
from fastapi.responses import JSONResponse
from typing import List , Dict , Optional , Annotated  , Literal
from pydantic import BaseModel , Field , computed_field
import json

app = FastAPI()

class Pateint(BaseModel):
    id     : Annotated[str , Field(..., description="This is the ID of the pateints")]
    name   : Annotated[str , Field(..., description="The name of the Pateint")]
    age    : Annotated[int , Field(... ,gt=0 , lt=65 , description="Age of the Pateint")]
    gender : Annotated[Literal['male' , 'female' , 'others'] , Field(..., description="select gender")]
    height : Annotated[float , Field(...,gt=0 , description="Heigth of the pateint in float")] 
    weight : Annotated[float , Field(... , gt=0 , description="The wieght will be greather then 0")] 
    
    @computed_field()
    @property
    def calculate_bmi(self) -> float:
        bmi = round(self.weight/(self.heigth**2) , 2)
        return bmi

class Updatepateint(BaseModel):
    name : Annotated[Optional[str] , Field(default=None)]
    city : Annotated[Optional[str] , Field(default=None)]
    age : Annotated[Optional[int] , Field(default=None , gt=0 , lt=65)]
    gender : Annotated[Optional[str] , Field(default=None)]
    height : Annotated[Optional[float], Field(default=None , gt=0)]
    weight : Annotated[Optional[float] , Field(default=None , gt=0)]
    
    
    
    
def load_data():
    with open('pateints.json' , 'r') as f:
        data = json.load(f)
        return data
def save_data(data):
    with open('pateints.json' , 'w') as f:
        json.dump(data , f)


@app.get("/")
def about():
    return ("This is Hospital Data")

@app.get('/pateint/{pateint_id}')
def load_pateint(pateint_id : str = Path(..., example="This is the ID of Pateint ")):
    data = load_data()
    for p in data["patients"]:
        if pateint_id == p["id"]:
            return p
        else:
            raise HTTPException(status_code=400 , detail="Pateint not Found")

@app.post('/create')
def create_acc(pateint : Pateint):
    #Load Data
    data = load_data()
    #Check if present
    for p in data["patients"]:
        if p["id"] == pateint.id:
            raise HTTPException(status_code=400 , detail="Already Present")
    
    #Convert pydantic into dict
    new_pateint = pateint.model_dump()
    #save 
    data["patients"].append(new_pateint)
    
    save_data(data)
    return JSONResponse(status_code=200 , content={"message" : "Pateint Created Sucessfull"})

@app.put('/edit/{pateint_id}')
def update_account(pateint_id : str , pateint_info : Updatepateint):
    data = load_data()
    for pateint in data["patients"]: #Every pateint detail 
        if pateint_id == pateint["id"]: #Matching Id detail of pateint
            #Get only provided Fields
            updated_data = pateint_info.model_dump(exclude_unset=True)
            #Update the Data
            pateint.update(updated_data)
            save_data(data)
            return JSONResponse(status_code=200 , content={"message" : "Pateint Updated"})
    raise HTTPException(status_code=401 , detail="Not Found!")


@app.delete("/delete/{patient_id}")
def delete_patient(patient_id: str):
    data = load_data()

    for i, patient in enumerate(data["patients"]):
        if patient["id"] == patient_id:
            deleted = data["patients"].pop(i)  # remove from list
            save_data(data)

            return JSONResponse(status_code=200,content={"message": "Patient deleted", "data": deleted})
    raise HTTPException(status_code=404, detail="Patient not found")