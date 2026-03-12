import os
import json
from sqlalchemy import text
from database import engine, SessionLocal, Base
import models
from auth import hash_password


def init_database():
    with engine.connect() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS public"))
        conn.execute(text("SET search_path TO public"))
        conn.commit()

    Base.metadata.create_all(bind=engine)
    print("✓ Tablas creadas correctamente")

    _add_contact_description_column()

    db = SessionLocal()
    try:
        _seed_admin(db)
        _seed_services(db)
        _seed_contact(db)
        _seed_about(db)
        _seed_projects(db)
        _seed_hero(db)
        _seed_social_links(db)
    finally:
        db.close()


def _add_contact_description_column():
    with engine.connect() as conn:
        result = conn.execute(text(
            "SELECT column_name FROM information_schema.columns "
            "WHERE table_name='contact_info' AND column_name='contact_description'"
        ))
        if result.fetchone() is None:
            conn.execute(text(
                "ALTER TABLE contact_info ADD COLUMN contact_description TEXT"
            ))
            conn.commit()
            print("✓ Columna contact_description añadida a contact_info")
        else:
            print("✓ Columna contact_description ya existe")

        conn.execute(text(
            "UPDATE contact_info SET contact_description = :desc "
            "WHERE contact_description IS NULL OR contact_description = ''"
        ), {"desc": "¿Tienes un proyecto en mente? Contáctanos y te ayudaremos a hacerlo realidad. Estamos disponibles para consultas, presupuestos y asesoramiento profesional."})
        conn.commit()


def _seed_admin(db):
    admin_email = os.getenv("ADMIN_EMAIL", "admin@stsg.com")
    admin_password = os.getenv("ADMIN_PASSWORD", "admin123")

    existing = db.query(models.User).filter(models.User.email == admin_email).first()
    if not existing:
        admin = models.User(
            email=admin_email,
            password=hash_password(admin_password),
        )
        db.add(admin)
        db.commit()
        print(f"✓ Admin creado: {admin_email}")
    else:
        print(f"✓ Admin ya existe: {admin_email}")


def _seed_services(db):
    if db.query(models.Service).count() > 0:
        print("✓ Servicios ya existen")
        return

    default_services = [
        {"title": "Construcción de todo tipo de viviendas", "description": "Lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod tempor.", "icon": "🏠", "order_index": 1},
        {"title": "Renovación y modernización", "description": "Ut enim ad minim veniam quis nostrud exercitation ullamco laboris nisi.", "icon": "🔨", "order_index": 2},
        {"title": "Adaptaciones de ático", "description": "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum.", "icon": "🏗️", "order_index": 3},
        {"title": "Construcción de garajes", "description": "Excepteur sint occaecat cupidatat non proident sunt in culpa qui officia.", "icon": "🚗", "order_index": 4},
        {"title": "Instalaciones públicas", "description": "Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit.", "icon": "🏢", "order_index": 5},
        {"title": "Acabados e instalaciones", "description": "Neque porro quisquam est qui dolorem ipsum quia dolor sit amet consectetur.", "icon": "✨", "order_index": 6},
    ]

    for s in default_services:
        db.add(models.Service(**s))
    db.commit()
    print("✓ Servicios por defecto creados")


def _seed_contact(db):
    if db.query(models.ContactInfo).count() > 0:
        print("✓ Info de contacto ya existe")
        return

    db.add(models.ContactInfo(
        phone="+48 601 908 812",
        email="contact@stsgcalidadtotal.com",
        address="Lorem ipsum 123, Ciudad Regional, País",
        maps_url="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3846.123456789!2d-75.7298!3d-14.0678!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x9110f0a0a0a0a0a1%3A0x1234567890abcdef!2sIca%2C%20Peru!5e0!3m2!1ses!2spe!4v1234567890",
        contact_description="¿Tienes un proyecto en mente? Contáctanos y te ayudaremos a hacerlo realidad. Estamos disponibles para consultas, presupuestos y asesoramiento profesional.",
    ))
    db.commit()
    print("✓ Info de contacto creada")


def _seed_about(db):
    if db.query(models.AboutContent).count() > 0:
        print("✓ Contenido 'Sobre nosotros' ya existe")
        return

    db.add(models.AboutContent(
        tag="QUIÉNES SOMOS",
        title="20 Años Construyendo el Futuro de Nuestra Región",
        paragraph1="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.",
        paragraph2="Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident sunt in culpa.",
        image_url="https://images.unsplash.com/photo-1541888946425-d81bb19240f5?w=800&q=80&fit=crop",
    ))
    db.commit()
    print("✓ Contenido 'Sobre nosotros' creado")


def _seed_projects(db):
    if db.query(models.Project).count() > 0:
        print("✓ Proyectos ya existen")
        return

    default_projects = [
        {
            "title": "Casa unifamiliar Krzycko",
            "category": "Viviendas",
            "description": "Lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod.",
            "full_description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
            "image": "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=800&q=80&fit=crop",
            "images": json.dumps([
                "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=800&q=80&fit=crop",
                "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=800&q=80&fit=crop",
                "https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?w=800&q=80&fit=crop",
                "https://images.unsplash.com/photo-1600585154526-990dced4db0d?w=800&q=80&fit=crop",
            ]),
            "year": "2023",
        },
        {
            "title": "Recepción Hotel WorkTravel",
            "category": "Hoteles",
            "description": "Lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod.",
            "full_description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.",
            "image": "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800&q=80&fit=crop",
            "images": json.dumps([
                "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800&q=80&fit=crop",
                "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800&q=80&fit=crop",
                "https://images.unsplash.com/photo-1590490360182-c33d57733427?w=800&q=80&fit=crop",
            ]),
            "year": "2023",
        },
        {
            "title": "Garaje subterráneo para edificio",
            "category": "Garajes",
            "description": "Lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod.",
            "full_description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore.",
            "image": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800&q=80&fit=crop",
            "images": json.dumps([
                "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800&q=80&fit=crop",
                "https://images.unsplash.com/photo-1486006920555-c77dcf18193c?w=800&q=80&fit=crop",
                "https://images.unsplash.com/photo-1573348722427-f1d6819fdf98?w=800&q=80&fit=crop",
                "https://images.unsplash.com/photo-1621929747188-0b4dc28498d2?w=800&q=80&fit=crop",
            ]),
            "year": "2022",
        },
        {
            "title": "Villa familiar de dos pisos",
            "category": "Viviendas",
            "description": "Lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod.",
            "full_description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Excepteur sint occaecat cupidatat non proident sunt in culpa qui officia.",
            "image": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800&q=80&fit=crop",
            "images": json.dumps([
                "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800&q=80&fit=crop",
                "https://images.unsplash.com/photo-1600566753086-00f18fb6b3ea?w=800&q=80&fit=crop",
                "https://images.unsplash.com/photo-1600573472592-401b489a3cdc?w=800&q=80&fit=crop",
            ]),
            "year": "2023",
        },
        {
            "title": "Complejo de apartamentos moderno",
            "category": "Edificios",
            "description": "Lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod.",
            "full_description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Nemo enim ipsam voluptatem quia voluptas sit aspernatur.",
            "image": "https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?w=800&q=80&fit=crop",
            "images": json.dumps([
                "https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?w=800&q=80&fit=crop",
                "https://images.unsplash.com/photo-1460317442991-0ec209397118?w=800&q=80&fit=crop",
                "https://images.unsplash.com/photo-1486325212027-8081e485255e?w=800&q=80&fit=crop",
                "https://images.unsplash.com/photo-1515263487990-61b07816b324?w=800&q=80&fit=crop",
            ]),
            "year": "2022",
        },
        {
            "title": "Renovación hotel boutique",
            "category": "Hoteles",
            "description": "Lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod.",
            "full_description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Neque porro quisquam est qui dolorem ipsum quia dolor sit amet.",
            "image": "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800&q=80&fit=crop",
            "images": json.dumps([
                "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800&q=80&fit=crop",
                "https://images.unsplash.com/photo-1582719508461-905c673771fd?w=800&q=80&fit=crop",
                "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=800&q=80&fit=crop",
            ]),
            "year": "2021",
        },
    ]

    for p in default_projects:
        db.add(models.Project(**p))
    db.commit()
    print("✓ Proyectos por defecto creados")


def _seed_hero(db):
    if db.query(models.HeroContent).count() > 0:
        print("✓ Hero content ya existe")
        return

    db.add(models.HeroContent(
        title="Construyendo Tu Visión, Un Proyecto a la Vez",
        subtitle="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Expertos regionales en construcción residencial y comercial desde 2003.",
        image_url="https://images.unsplash.com/photo-1504307651254-35680f356dfd?w=1600&q=80",
        button1_text="Ver Servicios",
        button2_text="Ver Proyectos",
    ))
    db.commit()
    print("✓ Hero content creado")


def _seed_social_links(db):
    if db.query(models.SocialLink).count() > 0:
        print("✓ Social links ya existen")
        return

    default_links = [
        {"network_name": "Facebook", "url": "https://www.facebook.com/STSGCalidadTotal", "icon": "facebook", "order_index": 1},
        {"network_name": "TikTok", "url": "https://www.tiktok.com/@STSGCalidadTotal", "icon": "tiktok", "order_index": 2},
        {"network_name": "Instagram", "url": "https://www.instagram.com/STSGCalidadTotal", "icon": "instagram", "order_index": 3},
    ]

    for link in default_links:
        db.add(models.SocialLink(**link))
    db.commit()
    print("✓ Social links creados")
