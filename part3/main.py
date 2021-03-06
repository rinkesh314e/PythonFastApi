from fastapi import FastAPI, Request, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import Optional
from utils import read_json
from uuid import uuid4
from fastapi.encoders import jsonable_encoder
import requests as rq
import json
from routers import providers


app = FastAPI()
app.include_router(providers.router)
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@ app.get("/", response_class=HTMLResponse)
def home(request: Request):
    healthcare_providers = read_json()
    return templates.TemplateResponse("base.html", {"request": request, "data": healthcare_providers})


# helper routes to call api endpoints
_PROVIDERS = "http://localhost:8000/providers/"  # api endpoint


# using .get("/providers/")
@app.get("/getallproviders/", response_class=HTMLResponse)
def get_all_healthcare_providers(request: Request):
    api_response = rq.get(_PROVIDERS).json()
    return templates.TemplateResponse("getAll.html", {"request": request, "data": api_response})


# using .get("/providers/{p_id}")
@app.get("/search", response_class=HTMLResponse)
def provider_search(request: Request):
    return templates.TemplateResponse('search.html', {"request": request, "flag": 1, "data": None})
\

# using .get("/providers/{p_id}")
@app.post("/search", response_class=HTMLResponse)
def provider_search(request: Request, p_id: str = Form(...)):
    api_response = rq.get(_PROVIDERS+p_id).json()
    return templates.TemplateResponse("search.html", {"request": request, "flag": 0, "data": api_response})


# using .post("/providers/")
@app.get("/addproviders", response_class=HTMLResponse)
def add_healthcare_provider_form(request: Request):
    return templates.TemplateResponse('add.html', {"request": request, "flag": 1})


# using .post("/providers/")
@app.post("/addproviders", response_class=HTMLResponse)
def add_healthcare_provider_form(request: Request, active: Optional[bool] = Form(None), name: str = Form(...),
                                 qualification: str = Form(...), speciality: str = Form(...), phone: str = Form(...), department: Optional[str] = Form(None),
                                 organization: str = Form(...), location: Optional[str] = Form(None), address: str = Form(...)
                                 ):
    new_post = {'providerID': jsonable_encoder(uuid4()), 'active': active, 'name': name, 'qualification': qualification, 'speciality': speciality,
                'phone': phone, 'department': department, 'organization': organization, 'location': location, 'address': address}
    api_response = rq.post(_PROVIDERS, data=json.dumps(new_post)).status_code
    return templates.TemplateResponse('add.html', {"request": request, "data": api_response, "flag": 0})


# using .put("/providers/{p_id}")
@app.get("/update", response_class=HTMLResponse)
def update_healthcare_provider_form(request: Request, p_id: str = "None"):
    print(p_id)
    if p_id == "None":
        return templates.TemplateResponse("update.html", {"request": request, "flag": 1})
    else:
        healthcare_providers = read_json()
        post = healthcare_providers.get(p_id, None)
        return templates.TemplateResponse("update.html", {"request": request, "flag": 0, "p_id": p_id, "post": post, "data": -1})


# using .put("/providers/{p_id}")
@app.post("/update", response_class=RedirectResponse, status_code=302)
def update_healthcare_provider_form(p_id: str = Form(...)):
    return 'http://localhost:8000/update?p_id=' + str(p_id)


# using .put("/providers/{p_id}")
@app.post("/updateform/", response_class=HTMLResponse)
def update_healthcare_provider_formid(request: Request, providerID: str = Form(...), active: Optional[bool] = Form(None), name: str = Form(...),
                                      qualification: str = Form(...), speciality: str = Form(...), phone: str = Form(...), department: Optional[str] = Form(None),
                                      organization: str = Form(...), location: Optional[str] = Form(None), address: str = Form(...)
                                      ):
    new_post = {'providerID': providerID, 'active': active, 'name': name, 'qualification': qualification, 'speciality': speciality,
                'phone': phone, 'department': department, 'organization': organization, 'location': location, 'address': address}
    api_response = rq.put(_PROVIDERS + str(providerID),
                          data=json.dumps(new_post)).status_code
    return templates.TemplateResponse('update.html', {"request": request, "data": api_response, "flag": -1})


# using .delete("/providers/{p_id}")
@app.get("/deleteprovider", response_class=HTMLResponse)
def delete_healthcare_provider_form(request: Request):
    return templates.TemplateResponse('delete.html', {"request": request})


# using .delete("/providers/{p_id}")
@app.post("/deleteprovider", response_class=HTMLResponse)
def delete_healthcare_provider_form(request: Request, p_id: str = Form(...)):
    api_response = rq.delete(_PROVIDERS+p_id).status_code
    return templates.TemplateResponse('delete.html', {"request": request, "response": api_response})
