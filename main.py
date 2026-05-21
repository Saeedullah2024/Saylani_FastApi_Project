from fastapi import FastAPI, HTTPException , Path , HTTPException ,Query
import json
app = FastAPI()

def load_file():
    with open("pateints.json"  , "r") as f:
        data = json.load(f)
        return data


@app.get("/")
def message():
    return {"Message" : "FastApi Testing"}

@app.get("/about")
def about():
    return {"University" : "Dawood University of Engineering"}

@app.get("/info")
def information():
    print("The product is about fastApi")

@app.get("/details")
def view_data():
    data = load_file()
    return data

@app.get("/pateint/{pateint_id}")
def view_pateint(pateint_id: str = Path(..., description="This is the Customer ID " , example="P1")):

    data = load_file()

    for patient in data["patients"]:

        if patient["id"] == pateint_id:
            return patient
        raise HTTPException(status_code=404 , detail="Pateint not Found")

@app.get("/sort")
def sort_pateint(sort_by : str = Query(..., description="Sort on basis of Disease or Gender"),
                 order   : str = Query('asc' , description="Asc order or desc order")):
    sort_values = ["age"]
    if sort_by not in sort_values:
        raise HTTPException(status_code=400 , detail=f"The sorting order is not in {sort_values}")
    order_block = ["asc" , "desc"]
    if order not in order_block:
        raise HTTPException(status_code=400 , detail=f"The order is not in {order_block}")
    data = load_file()
    sort_order = True if order=="desc" else False
    sorted_data = sorted(data["patients"] , key=lambda x : x.get(sort_by , 0) , reverse=sort_order)
    return sorted_data