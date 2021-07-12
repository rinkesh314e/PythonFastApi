from fastapi import FastAPI, Request, HTTPException, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import Optional
from schema import HealthcareProvider
from utils import read_json, write_json
import requests


app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@ app.get("/", response_class=HTMLResponse)
def home(request: Request):
    healthcare_providers = read_json()
    return templates.TemplateResponse("base.html", {"request": request, "data": healthcare_providers})


@ app.get('/providers/', response_class=HTMLResponse)
def get_healthcare_providers(request: Request):
    healthcare_providers = read_json()
    # return healthcare_providers
    return templates.TemplateResponse("getAll.html", {"request": request, "data": healthcare_providers})


@ app.get('/providers/{p_id}')
def get_healthcare_provider(p_id: int, request: Request):
    healthcare_providers = read_json()
    if healthcare_providers.get(str(p_id), None) is None:
        raise HTTPException(status_code=404, detail="ProviderID not found")
    result = healthcare_providers.get(str(p_id), None)
    # return result
    return templates.TemplateResponse("search.html", {"request": request, "flag": 0, "data": result})

# add new provider


@app.post('/providers/', response_class=RedirectResponse, status_code=302)
def add_healthcare_provider(providerID: int = Form(...), active: Optional[bool] = Form(None), name: str = Form(...),
                            qualification: str = Form(...), speciality: str = Form(...), phone: str = Form(...), department: Optional[str] = Form(None),
                            organization: str = Form(...), location: Optional[str] = Form(None), address: str = Form(...)
                            ):
    new_post = HealthcareProvider(providerID=providerID, active=active, name=name, qualification=qualification, speciality=speciality, phone=phone,
                                  department=department, organization=organization, location=location, address=address)
    healthcare_providers = read_json()
    if healthcare_providers.get(str(p_id), None) is not None:
        raise HTTPException(
            status_code=422, detail="ProviderID already exists")
    new_post = new_post.dict()
    p_id = new_post['providerID']
    healthcare_providers[p_id] = new_post
    write_json(healthcare_providers)
    # return {"message": "provider added"}
    return "/providers/" + str(p_id)


@ app.put('/providers/{p_id}')
def update_healthcare_provider(p_id: int, providerID: int = Form(...), active: Optional[bool] = Form(None), name: str = Form(...),
                               qualification: str = Form(...), speciality: str = Form(...), phone: str = Form(...), department: Optional[str] = Form(None),
                               organization: str = Form(...), location: Optional[str] = Form(None), address: str = Form(...)
                               ):
    healthcare_providers = read_json()
    if healthcare_providers.get(str(p_id), None) is None:
        raise HTTPException(status_code=404, detail="ProviderID not found")
    new_post = HealthcareProvider(providerID=providerID, active=active, name=name, qualification=qualification, speciality=speciality, phone=phone,
                                  department=department, organization=organization, location=location, address=address)
    healthcare_providers[str(p_id)] = new_post.dict()
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
    # return templates.TemplateResponse('delete.html', {"request": request})

######################################################################################

# helper routes to call api endpoints


# using get('/providers/{p_id}')
@app.get("/search", response_class=HTMLResponse)
def provider_search(request: Request):
    return templates.TemplateResponse('search.html', {"request": request, "flag": 1, "data": None})


# using get('/providers/{p_id}')
@app.post("/search", response_class=RedirectResponse, status_code=302)
def provider_search(p_id: int = Form(...)):
    return "providers/" + str(p_id)


# using post("/providers")
@app.get("/addproviders", response_class=HTMLResponse)
def add_healthcare_provider_form(request: Request):
    return templates.TemplateResponse('add.html', {"request": request})


@app.get("/update", response_class=HTMLResponse)
def update_healthcare_provider_form(request: Request):
    return templates.TemplateResponse("update.html", {"request": request, "flag": 1})


@app.post("/update", response_class=RedirectResponse, status_code=302)
def update_healthcare_provider_form(p_id: int = Form(...)):
    return 'http://localhost:8000/updateform/' + str(p_id)


@app.get("/updateform/{p_id}", response_class=HTMLResponse)
def update_healthcare_provider_formid(p_id: int, request: Request):
    healthcare_providers = read_json()
    post = healthcare_providers.get(str(p_id), None)
    return templates.TemplateResponse("update.html", {"request": request, "flag": 0, "p_id": p_id, "post": post})


@app.post("/updateform/")
def update_healthcare_provider_formid(providerID: int = Form(...), active: Optional[bool] = Form(None), name: str = Form(...),
                                      qualification: str = Form(...), speciality: str = Form(...), phone: str = Form(...), department: Optional[str] = Form(None),
                                      organization: str = Form(...), location: Optional[str] = Form(None), address: str = Form(...)
                                      ):
    new_post = HealthcareProvider(providerID=providerID, active=active, name=name, qualification=qualification, speciality=speciality, phone=phone,
                                  department=department, organization=organization, location=location, address=address)
    new_post = new_post.dict()
    print(new_post)
    url = 'http://localhost:8000/providers/' + str(providerID)
    x = requests.put(url, data=new_post)
    return RedirectResponse(url, status_code=status.HTTP_303_SEE_OTHER)


@app.get("/deleteprovider", response_class=HTMLResponse)
def delete_healthcare_provider_form(request: Request):
    return templates.TemplateResponse('delete.html', {"request": request})


@app.post("/deleteprovider", response_class=HTMLResponse)
def delete_healthcare_provider_form(request: Request, p_id: int = Form(...)):
    result = str(p_id)
    url = 'http://localhost:8000/providers/' + result
    x = requests.delete(url)
    x = str(x)
    return templates.TemplateResponse('delete.html', {"request": request, "response": x[-5:-2]})
