"""Shared utilities for pydantic models

"""
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel
from humps import camelize

def to_camel_case(string):
    """ Convert a string to camelCase
    
    This is a wrapper function that is used by the pydantic
    models to covert the snake_case field names to camelCase
    for the JSON response.

    It's important to follow standards for both languages
    and make it as seamless as possible for developers to
    work in each environment
    """
    return camelize(string)

class AppBaseModel(BaseModel):
    """ Pydantic base model for applications

    This class is used to define the base model for all schema
    that we use in the Application, it configures pydantic to
    translate between camcelCase and snake_case for the JSON
    amongst other default settings.

    ORM mode will allow pydantic to translate SQLAlchemy results
    into serializable models.

    For a full set of options, see:
    https://pydantic-docs.helpmanual.io/usage/model_config/
    """
    class Config:
        alias_generator = to_camel_case
        allow_population_by_field_name = True
        orm_mode = True

class IdentityMixin(BaseModel):
    """ Identifier 

    This mixin is used to define the identifier field for all
    models that use UUID as identifiers, which is out preference
    for PostgreSQL.
    """
    id: UUID

class DateTimeMixin(BaseModel):
    """ Adds timestamps to relevant models

    Many of out models will have a created and updated timestamp
    this mixin will add those fields to the schemas
    """
    created_at: datetime
    updated_at: datetime
 