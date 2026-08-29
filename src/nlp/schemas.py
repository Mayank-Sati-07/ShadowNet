from pydantic import BaseModel, Field


class Person(BaseModel):
    name: str


class Location(BaseModel):
    name: str
    location_type: str | None = None


class Vehicle(BaseModel):
    registration_number: str


class Phone(BaseModel):
    number: str


class Organization(BaseModel):
    name: str


class Event(BaseModel):
    event_type: str
    date: str | None = None


class Relationship(BaseModel):
    source: str
    relation: str
    target: str
    date: str | None = None
    evidence: str | None = None


class FIRExtraction(BaseModel):

    fir_id: str

    persons: list[Person] = Field(
        default_factory=list
    )

    locations: list[Location] = Field(
        default_factory=list
    )

    vehicles: list[Vehicle] = Field(
        default_factory=list
    )

    phones: list[Phone] = Field(
        default_factory=list
    )

    organizations: list[Organization] = Field(
        default_factory=list
    )

    events: list[Event] = Field(
        default_factory=list
    )

    relationships: list[Relationship] = Field(
        default_factory=list
    )