from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import os

app = FastAPI()
JSON_FILE = "courses.json"

class Course(BaseModel):
    course_name: str
    year: str
    semester: str
    grade: str

@app.get("/courses")
async def get_courses():
    try:
        if not os.path.exists(JSON_FILE):
            return []
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/courses")
async def add_course(course: Course):
    try:
        if os.path.exists(JSON_FILE):
            with open(JSON_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = []
        
        new_course_dict = course.model_dump()
        data.append(new_course_dict)
        
        with open(JSON_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        return {"msg": "수강기록 추가 성공"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)