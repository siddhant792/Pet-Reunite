"""
Enum class
"""

from enum import Enum


class PetStatusEnum(Enum):
    REGISTERED = "registered"
    LOST = "lost"
    FOUND = "found"


class PetGenderEnum(Enum):
    MALE = "male"
    FEMALE = "female"


class PetShelterEnum(Enum):
    HOME = "home"
    ANIMAL_SHELTER = "animal_shelter"
