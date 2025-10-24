from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from models import SessionStatus


# Schémas pour User
class UserBase(BaseModel):
    device_id: str
    card_recto_url: Optional[str] = None
    card_verso_url: Optional[str] = None
    verified: bool = False


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Schémas pour Operator
class OperatorBase(BaseModel):
    name: str
    email: EmailStr
    role: str
    is_active: bool = True


class OperatorCreate(OperatorBase):
    password: str


class OperatorResponse(OperatorBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Schémas pour EmergencySession
class EmergencySessionBase(BaseModel):
    user_id: Optional[int] = None
    operator_id: Optional[int] = None
    status: SessionStatus = SessionStatus.en_attente
    photo_url: Optional[str] = None
    audio_url: Optional[str] = None
    transcript: Optional[str] = None
    ia_result: Optional[str] = None
    ia_reason: Optional[str] = None
    location_lat: Optional[float] = None
    location_lng: Optional[float] = None
    address: Optional[str] = None


class EmergencySessionCreate(EmergencySessionBase):
    pass


class EmergencySessionResponse(EmergencySessionBase):
    id: int
    created_at: datetime
    updated_at: datetime
    closed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Schémas pour SessionUpdate
class SessionUpdateBase(BaseModel):
    session_id: int
    update_type: str
    content_url: Optional[str] = None
    text: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class SessionUpdateCreate(SessionUpdateBase):
    pass


class SessionUpdateResponse(SessionUpdateBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Schémas pour Location
class LocationBase(BaseModel):
    session_id: int
    latitude: float
    longitude: float
    accuracy: Optional[float] = None


class LocationCreate(LocationBase):
    pass


class LocationResponse(LocationBase):
    id: int
    recorded_at: datetime

    class Config:
        from_attributes = True


# Schémas pour AILog
class AILogBase(BaseModel):
    session_id: int
    ai_version: Optional[str] = None
    input_summary: Optional[str] = None
    output_summary: Optional[str] = None


class AILogCreate(AILogBase):
    pass


class AILogResponse(AILogBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Schémas pour Call
class CallBase(BaseModel):
    session_id: int
    operator_id: Optional[int] = None
    call_type: str
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    duration: Optional[int] = None


class CallCreate(CallBase):
    pass


class CallResponse(CallBase):
    id: int

    class Config:
        from_attributes = True
