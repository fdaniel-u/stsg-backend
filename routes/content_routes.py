from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import distinct
from database import get_db
import models
from auth import get_current_user
from schemas import (
    ServiceCreate, ServiceUpdate, ServiceResponse,
    ContactInfoUpdate, ContactInfoResponse,
    AboutContentUpdate, AboutContentResponse,
    HeroContentUpdate, HeroContentResponse,
    SocialLinkCreate, SocialLinkUpdate, SocialLinkResponse,
)

router = APIRouter(prefix="/api/content")


@router.get("/services", response_model=list[ServiceResponse])
def get_services(db: Session = Depends(get_db)):
    return db.query(models.Service).order_by(models.Service.order_index).all()


@router.post("/services", response_model=ServiceResponse)
def create_service(
    data: ServiceCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = models.Service(
        title=data.title,
        description=data.description,
        icon=data.icon,
        order_index=data.order_index,
    )
    db.add(service)
    db.commit()
    db.refresh(service)
    return service


@router.put("/services/{service_id}", response_model=ServiceResponse)
def update_service(
    service_id: int,
    data: ServiceUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = db.query(models.Service).filter(models.Service.id == service_id).first()
    if not service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Servicio no encontrado")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(service, key, value)

    db.commit()
    db.refresh(service)
    return service


@router.delete("/services/{service_id}")
def delete_service(
    service_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = db.query(models.Service).filter(models.Service.id == service_id).first()
    if not service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Servicio no encontrado")

    db.delete(service)
    db.commit()
    return {"message": "Servicio eliminado"}


@router.get("/contact", response_model=ContactInfoResponse)
def get_contact(db: Session = Depends(get_db)):
    contact = db.query(models.ContactInfo).first()
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Info de contacto no encontrada")
    return contact


@router.put("/contact", response_model=ContactInfoResponse)
def update_contact(
    data: ContactInfoUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    contact = db.query(models.ContactInfo).first()
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Info de contacto no encontrada")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(contact, key, value)

    db.commit()
    db.refresh(contact)
    return contact


@router.get("/about", response_model=AboutContentResponse)
def get_about(db: Session = Depends(get_db)):
    about = db.query(models.AboutContent).first()
    if not about:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contenido no encontrado")
    return about


@router.put("/about", response_model=AboutContentResponse)
def update_about(
    data: AboutContentUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    about = db.query(models.AboutContent).first()
    if not about:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contenido no encontrado")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(about, key, value)

    db.commit()
    db.refresh(about)
    return about


@router.get("/hero", response_model=HeroContentResponse)
def get_hero(db: Session = Depends(get_db)):
    hero = db.query(models.HeroContent).first()
    if not hero:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hero content no encontrado")
    return hero


@router.put("/hero", response_model=HeroContentResponse)
def update_hero(
    data: HeroContentUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    hero = db.query(models.HeroContent).first()
    if not hero:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hero content no encontrado")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(hero, key, value)

    db.commit()
    db.refresh(hero)
    return hero


@router.get("/social", response_model=list[SocialLinkResponse])
def get_social_links(db: Session = Depends(get_db)):
    return db.query(models.SocialLink).filter(
        models.SocialLink.is_active == True
    ).order_by(models.SocialLink.order_index).all()


@router.get("/social/all", response_model=list[SocialLinkResponse])
def get_all_social_links(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return db.query(models.SocialLink).order_by(models.SocialLink.order_index).all()


@router.post("/social", response_model=SocialLinkResponse)
def create_social_link(
    data: SocialLinkCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    link = models.SocialLink(
        network_name=data.network_name,
        url=data.url,
        icon=data.icon,
        is_active=data.is_active,
        order_index=data.order_index,
    )
    db.add(link)
    db.commit()
    db.refresh(link)
    return link


@router.put("/social/{link_id}", response_model=SocialLinkResponse)
def update_social_link(
    link_id: int,
    data: SocialLinkUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    link = db.query(models.SocialLink).filter(models.SocialLink.id == link_id).first()
    if not link:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Red social no encontrada")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(link, key, value)

    db.commit()
    db.refresh(link)
    return link


@router.delete("/social/{link_id}")
def delete_social_link(
    link_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    link = db.query(models.SocialLink).filter(models.SocialLink.id == link_id).first()
    if not link:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Red social no encontrada")

    db.delete(link)
    db.commit()
    return {"message": "Red social eliminada"}


@router.get("/categories", response_model=list[str])
def get_categories(db: Session = Depends(get_db)):
    results = db.query(distinct(models.Project.category)).filter(
        models.Project.category != None,
        models.Project.category != "",
    ).order_by(models.Project.category).all()
    return [r[0] for r in results]
