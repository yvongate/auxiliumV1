from sqlalchemy import (
    Column, Integer, String, Boolean, Text, TIMESTAMP, 
    Float, ForeignKey, CheckConstraint, Index, Enum
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import enum


# Enum pour le statut des sessions
class SessionStatus(enum.Enum):
    en_attente = "en_attente"
    a_affecter = "a_affecter"
    en_cours_appel = "en_cours_appel"
    en_suivi = "en_suivi"
    cloture = "cloture"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    device_id = Column(Text, nullable=False, unique=True)
    card_recto_url = Column(Text)
    card_verso_url = Column(Text)
    verified = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    # Relations
    emergency_sessions = relationship("EmergencySession", back_populates="user")


class Operator(Base):
    __tablename__ = "operators"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    email = Column(Text, nullable=False, unique=True)
    password_hash = Column(Text, nullable=False)
    role = Column(Text, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    __table_args__ = (
        CheckConstraint("role IN ('operator', 'supervisor')", name="check_operator_role"),
    )

    # Relations
    emergency_sessions = relationship("EmergencySession", back_populates="operator")
    calls = relationship("Call", back_populates="operator")


class EmergencySession(Base):
    __tablename__ = "emergency_sessions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    operator_id = Column(Integer, ForeignKey("operators.id", ondelete="SET NULL"))
    status = Column(Enum(SessionStatus), default=SessionStatus.en_attente)
    photo_url = Column(Text)
    audio_url = Column(Text)
    transcript = Column(Text)
    ia_result = Column(Text)
    ia_reason = Column(Text)
    location_lat = Column(Float)
    location_lng = Column(Float)
    address = Column(Text)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
    closed_at = Column(TIMESTAMP(timezone=True))

    # Relations
    user = relationship("User", back_populates="emergency_sessions")
    operator = relationship("Operator", back_populates="emergency_sessions")
    session_updates = relationship("SessionUpdate", back_populates="session", cascade="all, delete-orphan")
    locations = relationship("Location", back_populates="session", cascade="all, delete-orphan")
    ai_logs = relationship("AILog", back_populates="session", cascade="all, delete-orphan")
    calls = relationship("Call", back_populates="session", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_session_status", "status"),
        Index("idx_session_user", "user_id"),
    )


class SessionUpdate(Base):
    __tablename__ = "session_updates"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey("emergency_sessions.id", ondelete="CASCADE"), nullable=False)
    update_type = Column(Text, nullable=False)  # photo, audio, position, message, call_started, call_ended
    content_url = Column(Text)
    text = Column(Text)
    latitude = Column(Float)
    longitude = Column(Float)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    # Relations
    session = relationship("EmergencySession", back_populates="session_updates")

    __table_args__ = (
        Index("idx_updates_session", "session_id"),
    )


class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey("emergency_sessions.id", ondelete="CASCADE"), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    accuracy = Column(Float)
    recorded_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    # Relations
    session = relationship("EmergencySession", back_populates="locations")


class AILog(Base):
    __tablename__ = "ai_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey("emergency_sessions.id", ondelete="CASCADE"))
    ai_version = Column(Text)
    input_summary = Column(Text)
    output_summary = Column(Text)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    # Relations
    session = relationship("EmergencySession", back_populates="ai_logs")


class Call(Base):
    __tablename__ = "calls"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey("emergency_sessions.id", ondelete="CASCADE"))
    operator_id = Column(Integer, ForeignKey("operators.id", ondelete="SET NULL"))
    call_type = Column(Text)
    started_at = Column(TIMESTAMP(timezone=True))
    ended_at = Column(TIMESTAMP(timezone=True))
    duration = Column(Integer)

    __table_args__ = (
        CheckConstraint("call_type IN ('visio', 'audio')", name="check_call_type"),
    )

    # Relations
    session = relationship("EmergencySession", back_populates="calls")
    operator = relationship("Operator", back_populates="calls")
