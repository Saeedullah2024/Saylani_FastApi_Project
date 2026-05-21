from pydantic import BaseModel , EmailStr , AnyUrl , Field , field_validator , model_validator
from typing import Dict , List , Optional , Annotated
from fastapi import FastAPI

app = FastAPI()


class user_info(BaseModel):
    name : str = Field(max_length=30)
    email : Optional[EmailStr] = None
    age : int = Optional[Field(default=None , gt=18 , lt=65)]
    linkedIN_URl : Optional[AnyUrl] = None
    roll_no : str 
    contact : Dict[str , str]
    allgergies : Optional[Annotated[List[str] , Field(max_length=2 , title="Name of the Pateint" , 
                                                    description="For Example (SaeedUllah , Saba Qamar)")]] = None
    married : Annotated[bool , Field(default=None , description='Is the Pateint Married or Not')]
    
    @model_validator()
    def model_check(cls , model):
        if model.age > 65:
            raise ValueError("Age should be between 18 - 65")
        return model #Should be return if all check
        
def user(pateint : user_info):

    print(pateint.name)
    print(pateint.roll_no)
    print(pateint.contact)
    print(pateint.allgergies)
    print(pateint.email)
    print(pateint.linkedIN_URl)

data = {"name" : "Saeedullah" , "roll_no" : "23-AI-11" , "contact":{"Phone":"03022" , "Whats":"03669"}}
pateint_data = user_info(**data)
pateint_data_print = user(pateint_data)
print(pateint_data_print)
