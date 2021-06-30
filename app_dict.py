from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import json

app = FastAPI()


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


class HealthcareProvider(BaseModel):
    providerID: int
    active: bool = True
    name: str
    qualification: str
    speciality: str
    phone: str
    department: Optional[str]
    organization: str
    location: Optional[str]
    address: str


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

