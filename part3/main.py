from fastapi import FastAPI, Request, HTTPException, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from typing import Optional
import json
import requests


app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


class HealthcareProvider(BaseModel):
    providerID: int = Field(..., ge=0, description="identifier id")
    active: bool = Field(True, example=True,
                         description="Record in active use or not")
    name: str = Field(..., example="YourName",
                      description="Name of the Provider")
    qualification: str = Field(..., example="qual1, qual2",
                               description="Comma separated qualification of the provider")
    speciality: str = Field(..., example="speciality1, speciality2",
                            description="Comma separated specialities")
    phone: str = Field(..., example="9876543210", max_length=15,
                       description="Number of Provider")
    department: Optional[str] = Field(
        None, example="depName", description="Department, if applicable")
    organization: str = Field(..., example="OrgaName",
                              description="Name of the Hospital/Clinic of the Provider")
    location: Optional[str] = Field(
        None, example="loc1, loc2", description="Location, if multiple locations")
    address: str = Field(..., example="address",
                         description="Address of Hospital")


def read_json():
    try:
        with open('./data/data_dict.json', 'r') as file:
            healthcare_providers = json.load(file)
    except IOError:
        healthcare_providers = {}
    return healthcare_providers


def write_json(healthcare_providers):
    try:
        with open('./data/data_dict.json', 'w+') as file:
            json.dump(healthcare_providers, file)
    except IOError as err:
        print(f'Error: {err}')


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
    result = healthcare_providers.get(str(p_id), None)
    return templates.TemplateResponse("getProvider.html", {"request": request, "data": result})


@app.post('/providers/', response_class=RedirectResponse, status_code=302)
def add_healthcare_provider(providerID: int = Form(...), active: bool = Form(...), name: str = Form(...),
                            qualification: str = Form(...), speciality: str = Form(...), phone: str = Form(...), department: Optional[str] = Form(None),
                            organization: str = Form(...), location: Optional[str] = Form(None), address: str = Form(...)
                            ):
    healthcare_providers = read_json()
    new_post = HealthcareProvider(providerID=providerID, active=active, name=name, qualification=qualification, speciality=speciality, phone=phone,
                                  department=department, organization=organization, location=location, address=address)
    new_post = new_post.dict()
    p_id = new_post['providerID']
    healthcare_providers[p_id] = new_post
    write_json(healthcare_providers)
    return "/providers"


@ app.put('/providers/{p_id}')
def update_healthcare_provider(p_id: int, providerID: int = Form(...), active: bool = Form(...), name: str = Form(...),
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
    return new_post.dict()


@ app.delete('/providers/{p_id}', response_class=HTMLResponse)
def delete_healthcare_provider(p_id: int, request: Request):
    healthcare_providers = read_json()
    if healthcare_providers.get(str(p_id), None) is None:
        raise HTTPException(status_code=404, detail="ProviderID not found")
    healthcare_providers.pop(str(p_id))
    write_json(healthcare_providers)
    return templates.TemplateResponse('delete.html', {"request": request})

################################################################################

# helper routes to call api endpoints


@app.get("/addproviders", response_class=HTMLResponse)
def add_healthcare_provider_form(request: Request):
    return templates.TemplateResponse('add.html', {"request": request})


@app.get("/search", response_class=HTMLResponse)
def provider_search(request: Request):
    return templates.TemplateResponse('search.html', {"request": request})


@app.post("/search", response_class=RedirectResponse, status_code=302)
def provider_search(request: Request, p_id: int = Form(...)):
    result = str(p_id)
    url = 'http://localhost:8000/providers/' + result
    return url


@app.get("/update", response_class=HTMLResponse)
def update_healthcare_provider_form(request: Request):
    return templates.TemplateResponse("update.html", {"request": request})


@app.post("/update", response_class=RedirectResponse, status_code=302)
def update_healthcare_provider_form(request: Request, p_id: int = Form(...)):
    url = 'http://localhost:8000/updateprovider/' + str(p_id)
    return url


@app.get("/updateprovider/{p_id}", response_class=HTMLResponse)
def update_healthcare_provider_formid(p_id: int, request: Request):
    healthcare_providers = read_json()
    post = healthcare_providers.get(str(p_id), None)
    return templates.TemplateResponse("updateform.html", {"request": request, "p_id": p_id, "post": post})


@app.post("/updateprovider/")
def update_healthcare_provider_formid(providerID: int = Form(...), active: bool = Form(...), name: str = Form(...),
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
    # print(x[-5:-2])
    return templates.TemplateResponse('delete.html', {"request": request, "response": x[-5:-2]})