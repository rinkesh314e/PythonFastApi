from fastapi import APIRouter, HTTPException
from schema import HealthcareProvider
from uuid import UUID
from fastapi.encoders import jsonable_encoder
from utils import read_json, write_json, get_items


router = APIRouter(tags=["healthcare_providers"])


@router.get('/providers/')
def get_healthcare_providers(skip: int=0, limit: int = 10):
    healthcare_providers = read_json()
    healthcare_providers = get_items(healthcare_providers, skip, limit)
    return healthcare_providers


@router.get('/providers/{p_id}')
def get_healthcare_provider(p_id: UUID):
    p_id = str(p_id)
    healthcare_providers = read_json()
    if healthcare_providers.get(p_id, None) is None:
        raise HTTPException(status_code=404, detail="ProviderID not found")
    return healthcare_providers[str(p_id)]


@router.post('/providers/')
def add_healthcare_provider(post: HealthcareProvider):
    post = post.dict()
    post["providerID"] = jsonable_encoder(post["providerID"])
    healthcare_providers = read_json()
    if healthcare_providers.get(post['providerID'], None) is not None:
        raise HTTPException(
            status_code=422, detail="ProviderID already exists")
    healthcare_providers[post['providerID']] = post
    write_json(healthcare_providers)
    return {"message": "Added new provider"}


@router.put('/providers/{p_id}')
def update_healthcare_provider(p_id: UUID, post: HealthcareProvider):
    post = post.dict()
    post["providerID"] = jsonable_encoder(post["providerID"])
    p_id = str(p_id)
    healthcare_providers = read_json()
    if healthcare_providers.get(p_id, None) is None:
        raise HTTPException(status_code=404, detail="ProviderID not found")
    healthcare_providers[p_id] = post
    write_json(healthcare_providers)
    return {"message": "successfully updated"}


@router.delete('/providers/{p_id}')
def delete_healthcare_provider(p_id: UUID):
    p_id = str(p_id)
    healthcare_providers = read_json()
    if healthcare_providers.get(p_id, None) is None:
        raise HTTPException(status_code=404, detail="ProviderID not found")
    healthcare_providers.pop(p_id)
    write_json(healthcare_providers)
    return {"message": "provider successfully deleted"}
