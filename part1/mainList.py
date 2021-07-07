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


healthcare_providers = []


@app.get('/providers/')
def get_healthcare_providers():
    return healthcare_providers


@app.get('/providers/{p_id}')
def get_healthcare_provider(p_id: int):
    result = next(
        (provider for provider in healthcare_providers if provider['providerID'] == p_id), None)
    if result is None:
        raise HTTPException(status_code=404, detail="ProviderID not found")
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
        raise HTTPException(status_code=404, detail="ProviderID not found")
    healthcare_providers[index] = post.dict()
    return update_dict


@app.delete('/providers/{p_id}')
def delete_healthcare_provider(p_id: int):
    healthcare_providers[:] = [provider
                               for provider in healthcare_providers
                               if not provider['providerID'] == p_id]
    return healthcare_providers
