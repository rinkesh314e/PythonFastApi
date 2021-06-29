from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional


app = FastAPI()


healthcare_providers = []

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
    return healthcare_providers


@app.get('/providers/{p_id}')
def get_healthcare_provider(p_id: int):
    result = next((provider for provider in healthcare_providers if provider['providerID'] == p_id), None)
    if result is None:
        return {"error": "ProviderId not found"}
    return result


@app.post('/providers/')
def add_healthcare_provider(post: HealthcareProvider):
    healthcare_providers.append(post.dict())
    return healthcare_providers


@app.put('/providers/{p_id}')
def update_healthcare_provider(p_id: int, post: HealthcareProvider):
    index, update_dict = next(((idx, provider) 
                            for idx, provider in enumerate(healthcare_providers) 
                            if provider['providerID'] == p_id), None)
    if update_dict is None:
        return {"error": "ProviderId not found"}
    healthcare_providers[index] = post.dict()
    return update_dict



@app.delete('/providers/{p_id}')
def delete_healthcare_provider(p_id: int):
    healthcare_providers[:] = [provider 
                                for provider in healthcare_providers 
                                if not provider['providerID']==p_id]
    return healthcare_providers
