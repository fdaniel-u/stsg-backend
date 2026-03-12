from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.sql import func
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255))
    created_at = Column(DateTime, default=func.now())


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False)
    description = Column(Text)
    full_description = Column(Text)
    image = Column(String(500))
    images = Column(Text)
    year = Column(String(10))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    icon = Column(String(100))
    order_index = Column(Integer, default=0)
    created_at = Column(DateTime, default=func.now())


class ContactInfo(Base):
    __tablename__ = "contact_info"

    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String(100))
    email = Column(String(255))
    address = Column(Text)
    maps_url = Column(Text)
    contact_description = Column(Text)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class AboutContent(Base):
    __tablename__ = "about_content"

    id = Column(Integer, primary_key=True, index=True)
    tag = Column(String(100))
    title = Column(String(255))
    paragraph1 = Column(Text)
    paragraph2 = Column(Text)
    image_url = Column(String(500))
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class HeroContent(Base):
    __tablename__ = "hero_content"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500))
    subtitle = Column(Text)
    image_url = Column(String(500))
    button1_text = Column(String(100))
    button2_text = Column(String(100))
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class SocialLink(Base):
    __tablename__ = "social_links"

    id = Column(Integer, primary_key=True, index=True)
    network_name = Column(String(100), nullable=False)
    url = Column(String(500), nullable=False)
    icon = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)
    order_index = Column(Integer, default=0)
    created_at = Column(DateTime, default=func.now())
