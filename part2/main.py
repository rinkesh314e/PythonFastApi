from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
import json

app = FastAPI()


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


@app.get("/")
def home():
    return "Greetings..."


@app.get('/providers/')
def get_healthcare_providers():
    healthcare_providers = read_json()
    return healthcare_providers


@app.get('/providers/{p_id}')
def get_healthcare_provider(p_id: int):
    healthcare_providers = read_json()
    result = healthcare_providers.get(str(p_id), None)
    if result is None:
        raise HTTPException(status_code=404, detail="ProviderID not found")
    return result


@app.post('/providers/')
def add_healthcare_provider(post: HealthcareProvider):
    healthcare_providers = read_json()
    new_post = post.dict()
    healthcare_providers[new_post['providerID']] = new_post
    write_json(healthcare_providers)
    return healthcare_providers


@app.put('/providers/{p_id}')
def update_healthcare_provider(p_id: int, post: HealthcareProvider):
    healthcare_providers = read_json()
    if healthcare_providers.get(str(p_id), None) is None:
        raise HTTPException(status_code=404, detail="ProviderID not found")
    healthcare_providers[str(p_id)] = post.dict()
    write_json(healthcare_providers)
    return post.dict()


@app.delete('/providers/{p_id}')
def delete_healthcare_provider(p_id: int):
    healthcare_providers = read_json()
    if healthcare_providers.get(str(p_id), None) is None:
        raise HTTPException(status_code=404, detail="ProviderID not found")
    healthcare_providers.pop(str(p_id))
    write_json(healthcare_providers)
    return healthcare_providers
