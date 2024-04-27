from AoE2ScenarioParser.datasets.buildings import BuildingInfo

from src.implement.events.events import Event

SectionType = dict[BuildingInfo, list[list[Event]]]

# Building, the building size, the reservation size
AiBuildingDetails = tuple[BuildingInfo, int, int]

# The spawn types with the amount of spawn tries
BuildingSpawnAttempt = tuple[list[AiBuildingDetails], int, float]
TownBuildingSpawnAttempts = list[BuildingSpawnAttempt]
