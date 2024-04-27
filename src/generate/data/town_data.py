from AoE2ScenarioParser.datasets.buildings import BuildingInfo

from src.generate.types.types import AiBuildingDetails, TownBuildingSpawnAttempts

ai_sws_buildings_spawns: list[AiBuildingDetails] = [
    (BuildingInfo.SIEGE_WORKSHOP, 4, 6),
]

ai_cst_buildings_spawns: list[AiBuildingDetails] = [
    (BuildingInfo.CASTLE, 4, 6),
]

ai_3x3_buildings_spawns: list[AiBuildingDetails] = [
    # @formatter:off
    (BuildingInfo.BARRACKS,      3, 5),
    (BuildingInfo.STABLE,        3, 5),
    (BuildingInfo.ARCHERY_RANGE, 3, 5),
    # @formatter:on
]

ai_mns_buildings_spawns: list[AiBuildingDetails] = [
    # @formatter:off
    (BuildingInfo.MONASTERY,     3, 5),
    # @formatter:on
]

ai_2x2_buildings_spawns: list[AiBuildingDetails] = [
    (BuildingInfo.HOUSE,         2, 2),
]

ai_1x1_buildings_spawns: list[AiBuildingDetails] = [
    (BuildingInfo.WATCH_TOWER, 1, 1),
]

spawn_attempts: TownBuildingSpawnAttempts = [
    # @formatter:off
    (ai_cst_buildings_spawns,   1, 0.1),
    (ai_sws_buildings_spawns,   5, 0.2),
    (ai_mns_buildings_spawns,   3, 0.5),
    (ai_3x3_buildings_spawns,  10, 1.0),
    (ai_2x2_buildings_spawns,  20, 1.0),
    (ai_1x1_buildings_spawns,  20, 0.0),
    # @formatter:on
]
