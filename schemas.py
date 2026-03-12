import json
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, field_validator


class UserLogin(BaseModel):
    email: str
    password: str


class ProjectCreate(BaseModel):
    title: str
    category: str
    description: str
    full_description: str
    image: str
    images: list[str]
    year: str


class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    full_description: Optional[str] = None
    image: Optional[str] = None
    images: Optional[list[str]] = None
    year: Optional[str] = None


class ProjectResponse(BaseModel):
    id: int
    title: str
    category: str
    description: str
    full_description: str
    image: str
    images: list[str]
    year: str
    created_at: datetime

    @field_validator("images", mode="before")
    @classmethod
    def parse_images(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except Exception:
                return []
        if v is None:
            return []
        return v

    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ServiceCreate(BaseModel):
    title: str
    description: str
    icon: str = ""
    order_index: int = 0


class ServiceUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    order_index: Optional[int] = None


class ServiceResponse(BaseModel):
    id: int
    title: str
    description: str
    icon: str
    order_index: int
    created_at: datetime

    @field_validator("icon", mode="before")
    @classmethod
    def default_icon(cls, v):
        return v or ""

    model_config = {"from_attributes": True}


class ContactInfoCreate(BaseModel):
    phone: str
    email: str
    address: str
    maps_url: str
    contact_description: str = ""


class ContactInfoUpdate(BaseModel):
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    maps_url: Optional[str] = None
    contact_description: Optional[str] = None


class ContactInfoResponse(BaseModel):
    id: int
    phone: str
    email: str
    address: str
    maps_url: str
    contact_description: str
    updated_at: datetime

    @field_validator("phone", "email", "address", "maps_url", "contact_description", mode="before")
    @classmethod
    def default_empty(cls, v):
        return v or ""

    model_config = {"from_attributes": True}


class AboutContentCreate(BaseModel):
    tag: str
    title: str
    paragraph1: str
    paragraph2: str
    image_url: str


class AboutContentUpdate(BaseModel):
    tag: Optional[str] = None
    title: Optional[str] = None
    paragraph1: Optional[str] = None
    paragraph2: Optional[str] = None
    image_url: Optional[str] = None


class AboutContentResponse(BaseModel):
    id: int
    tag: str
    title: str
    paragraph1: str
    paragraph2: str
    image_url: str
    updated_at: datetime

    @field_validator("tag", "title", "paragraph1", "paragraph2", "image_url", mode="before")
    @classmethod
    def default_empty(cls, v):
        return v or ""

    model_config = {"from_attributes": True}


class HeroContentCreate(BaseModel):
    title: str
    subtitle: str
    image_url: str
    button1_text: str = "Ver Servicios"
    button2_text: str = "Ver Proyectos"


class HeroContentUpdate(BaseModel):
    title: Optional[str] = None
    subtitle: Optional[str] = None
    image_url: Optional[str] = None
    button1_text: Optional[str] = None
    button2_text: Optional[str] = None


class HeroContentResponse(BaseModel):
    id: int
    title: str
    subtitle: str
    image_url: str
    button1_text: str
    button2_text: str
    updated_at: datetime

    @field_validator("title", "subtitle", "image_url", "button1_text", "button2_text", mode="before")
    @classmethod
    def default_empty(cls, v):
        return v or ""

    model_config = {"from_attributes": True}


class SocialLinkCreate(BaseModel):
    network_name: str
    url: str
    icon: str
    is_active: bool = True
    order_index: int = 0


class SocialLinkUpdate(BaseModel):
    network_name: Optional[str] = None
    url: Optional[str] = None
    icon: Optional[str] = None
    is_active: Optional[bool] = None
    order_index: Optional[int] = None


class SocialLinkResponse(BaseModel):
    id: int
    network_name: str
    url: str
    icon: str
    is_active: bool
    order_index: int
    created_at: datetime

    model_config = {"from_attributes": True}
