from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import json
import requests
from jsonReader import clean_data, extract_year_data, extract_month_data, fetch_youtuber_data

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):

    contents = await file.read()
    contents_as_json_string = contents.decode('utf8')
    contents_as_json = json.loads(contents_as_json_string)

    data = contents_as_json
    #data = json.load(open(file.filename, encoding="utf8"))
    cleaned_data = clean_data(data=data)
    year_data = extract_year_data(cleaned_data)
    month_data = []
    for month in range(1, 13):
        current_month_data = extract_month_data(data=cleaned_data, month=month)
        month_data.append(current_month_data)

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "data": {
            "year": year_data,
            "month": month_data
        }
    }
    
@app.get("/youtubers")
async def get_youtuber_data(id: str):
    return fetch_youtuber_data(id=id)