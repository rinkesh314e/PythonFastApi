from pydantic import BaseModel, Field
from typing import Optional


class HealthcareProvider(BaseModel):
    providerID: int = Field(..., ge=0, description="identifier id")
    active: Optional[bool] = Field(True, description="Record in active use or not")
    name: str = Field(..., description="Name of the Provider")
    qualification: str = Field(..., description="Comma separated qualification of the provider")
    speciality: str = Field(..., description="Comma separated specialities")
    phone: str = Field(..., max_length=15, regex="(\+[\d]{2})?[\d]{10}", description="Number of Provider")
    department: Optional[str] = Field(None, example="depName", description="Department, if applicable")
    organization: str = Field(..., description="Name of the Hospital/Clinic of the Provider")
    location: Optional[str] = Field(None, description="Location, if multiple locations")
    address: str = Field(..., description="Address of Hospital")

    class Config:
        schema_extra = {
            "example": {
                "active": True,
                "name": "Jon Doe",
                "qualification": "MBBS, MD",
                "speciality": "Surgery, Diagnostician",
                "phone": "+918759641230",
                "department": "ER, Medicine",
                "organization": "OrganizationA",
                "location": "loc1, loc2",
                "address": "Address-New",
            }
        }
