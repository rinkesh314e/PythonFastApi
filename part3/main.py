from fastapi import FastAPI, Request, HTTPException, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import Optional
from schema import HealthcareProvider
from utils import read_json, write_json
import requests as rq
import json


app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@ app.get("/", response_class=HTMLResponse)
def home(request: Request):
    healthcare_providers = read_json()
    return templates.TemplateResponse("base.html", {"request": request, "data": healthcare_providers})


@ app.get('/providers/')
def get_healthcare_providers():
    healthcare_providers = read_json()
    return healthcare_providers


@ app.get('/providers/{p_id}')
def get_healthcare_provider(p_id: int):
    healthcare_providers = read_json()
    if healthcare_providers.get(str(p_id), None) is None:
        raise HTTPException(status_code=404, detail="ProviderID not found")
    result = healthcare_providers.get(str(p_id), None)
    return result


@ app.post('/providers/')
def add_healthcare_provider(post: HealthcareProvider):
    healthcare_providers = read_json()
    post = post.dict()
    if healthcare_providers.get(str(post['providerID']), None) is not None:
        raise HTTPException(
            status_code=422, detail="ProviderID already exists")
    healthcare_providers[post['providerID']] = post
    write_json(healthcare_providers)
    return {"message": "Added new provider"}


@app.put('/providers/{p_id}')
def update_healthcare_provider(p_id: int, post: HealthcareProvider):
    healthcare_providers = read_json()
    if healthcare_providers.get(str(p_id), None) is None:
        raise HTTPException(status_code=404, detail="ProviderID not found")
    healthcare_providers[str(p_id)] = post.dict()
    write_json(healthcare_providers)
    return {"message": "successfully updated"}


@ app.delete('/providers/{p_id}')
def delete_healthcare_provider(p_id: int):
    healthcare_providers = read_json()
    if healthcare_providers.get(str(p_id), None) is None:
        raise HTTPException(status_code=404, detail="ProviderID not found")
    healthcare_providers.pop(str(p_id))
    write_json(healthcare_providers)
    return {"message": "provider successfully deleted"}


######################################################################################
# helper routes to call api endpoints
_PROVIDERS = "http://localhost:8000/providers/"  # api endpoint


# using .get("/providers/")
@app.get("/getallproviders", response_class=HTMLResponse)
def get_all_healthcare_providers(request: Request):
    api_response = rq.get(_PROVIDERS).json()
    return templates.TemplateResponse("getAll.html", {"request": request, "data": api_response})


# using .get("/providers/{p_id}")
@app.get("/search", response_class=HTMLResponse)
def provider_search(request: Request):
    return templates.TemplateResponse('search.html', {"request": request, "flag": 1, "data": None})


# using .get("/providers/{p_id}")
@app.post("/search", response_class=HTMLResponse)
def provider_search(request: Request, p_id: int = Form(...)):
    api_response = rq.get(_PROVIDERS+str(p_id)).json()
    return templates.TemplateResponse("search.html", {"request": request, "flag": 0, "data": api_response})


# using .post("/providers/")
@app.get("/addproviders", response_class=HTMLResponse)
def add_healthcare_provider_form(request: Request):
    return templates.TemplateResponse('add.html', {"request": request, "flag": 1})


# using .post("/providers/")
@app.post("/addproviders", response_class=HTMLResponse)
def add_healthcare_provider_form(request: Request, providerID: int = Form(...), active: Optional[bool] = Form(None), name: str = Form(...),
                                 qualification: str = Form(...), speciality: str = Form(...), phone: str = Form(...), department: Optional[str] = Form(None),
                                 organization: str = Form(...), location: Optional[str] = Form(None), address: str = Form(...)
                                 ):
    new_post = {'providerID': providerID, 'active': active, 'name': name, 'qualification': qualification, 'speciality': speciality,
                'phone': phone, 'department': department, 'organization': organization, 'location': location, 'address': address}
    api_response = rq.post(_PROVIDERS, data=json.dumps(new_post)).status_code
    return templates.TemplateResponse('add.html', {"request": request, "data": api_response, "flag": 0})


# using .put("/providers/{p_id}")
@app.get("/update", response_class=HTMLResponse)
def update_healthcare_provider_form(request: Request, p_id: int = -1):
    print(p_id)
    if p_id == -1:
        return templates.TemplateResponse("update.html", {"request": request, "flag": 1})
    else:
        healthcare_providers = read_json()
        post = healthcare_providers.get(str(p_id), None)
        return templates.TemplateResponse("update.html", {"request": request, "flag": 0, "p_id": p_id, "post": post, "data": -1})


# using .put("/providers/{p_id}")
@app.post("/update", response_class=RedirectResponse, status_code=302)
def update_healthcare_provider_form(p_id: int = Form(...)):
    return 'http://localhost:8000/update?p_id=' + str(p_id)


# using .put("/providers/{p_id}")
@app.post("/updateform/", response_class=HTMLResponse)
def update_healthcare_provider_formid(request: Request, providerID: int = Form(...), active: Optional[bool] = Form(None), name: str = Form(...),
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
def delete_healthcare_provider_form(request: Request, p_id: int = Form(...)):
    api_response = rq.delete(_PROVIDERS+str(p_id)).status_code
    return templates.TemplateResponse('delete.html', {"request": request, "response": api_response})
