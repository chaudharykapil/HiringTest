from fastapi import APIRouter, HTTPException, Query, Path
from bson import ObjectId
from fastapi.responses import JSONResponse
from pymongo.errors import DuplicateKeyError
from typing import List,Optional
from api.utils.DBManager import db
from api.models.models import StudentCreate, StudentUpdate, StudentResponse

routes = APIRouter()

def validate_id(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    return ObjectId(id)

@routes.get("/")
def hello():
    return JSONResponse({},status_code=200)

@routes.get("/students",response_model=List[StudentResponse],status_code=200)
def get_all_students(country:Optional[str] = Query(None),age:Optional[int] = Query(None)):
    
    querydata = {}
    if country:
        querydata["address.country"] = country
    if age:
        querydata["age"] = {"$gte":age}
    
    allstudents = db.students.find(querydata)
    data = [{"name":student["name"],"age":student["age"]} for student in allstudents.to_list()]
    print(data)
    return JSONResponse({"data":data},status_code=200)

@routes.post("/students",status_code=201,response_model=dict)
def add_new_user(student:StudentCreate):
    new_student = student.model_dump()
    try:
        result = db.students.insert_one(new_student)
        return JSONResponse({"id": str(result.inserted_id)},status_code=201)
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="Student with this data already exists")
    

@routes.get("/students/{id}",response_model=StudentResponse,status_code=200)
def get_student(id:str = Path(...)):
    std_id = validate_id(id)
    student = db.students.find_one({"_id":std_id})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    data = {"name":student["name"],"age":student["age"],"address":student["address"]}
    print(student)
    return JSONResponse(data,status_code=200)


@routes.patch("/students/{id}",status_code=204)
def update_user(update_student:StudentUpdate,id:str=Path(...)):
    std_id = validate_id(id)
    old_Std =  db.students.find_one({"_id": std_id})
    if not old_Std:
        raise HTTPException(status_code=404, detail="Student not found")
    old_addr = old_Std.get("address", {})
    update_data = {k:v for k,v in update_student.model_dump().items() if v is not None}
    if "address" in update_data:
        old_addr.update({k:v for k,v in update_data["address"].items() if v is not None}) 
        update_data["address"] = old_addr
            
    if not update_data:
        raise HTTPException(status_code=400, detail="No valid updates provided")
    result = db.students.update_one({"_id": std_id}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return



@routes.delete("/students/{id}",status_code=204)
def delete_user(id:str = Path(...)):
    std_id = validate_id(id)
    res = db.students.delete_one({"_id":std_id})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return

