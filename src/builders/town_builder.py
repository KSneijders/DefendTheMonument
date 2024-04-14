import random
from typing import Iterable

from AoE2ScenarioParser.datasets.buildings import BuildingInfo
from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.terrains import TerrainId
from AoE2ScenarioParser.objects.managers.unit_manager import UnitManager
from AoE2ScenarioParser.objects.support.area import Area
from AoE2ScenarioParser.objects.support.tile import Tile
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario

from src.types.types import TownBuildingSpawnAttempts, AiBuildingDetails


class TownBuilder:
    def __init__(self, spawn_attempts: TownBuildingSpawnAttempts):
        self.spawn_attempts: TownBuildingSpawnAttempts = spawn_attempts

    def apply(self, scenario: AoE2DEScenario) -> None:
        um, mm = scenario.unit_manager, scenario.map_manager

        # Find all castles of P8 (where to spawn towns)
        trees = set(tree.ID for tree in OtherInfo.trees())
        tree_terrains = set(TerrainId.tree_terrains())

        p8_castles = um.filter_units_by_const(unit_consts=[BuildingInfo.CASTLE.ID], player_list=[PlayerId.EIGHT])
        for castle in p8_castles:
            castle_centered = scenario.new.area().center(*castle.tile)
            town_area = castle_centered.copy().expand(20)

            units = um.get_units_in_area(**town_area.to_dict(prefix=''), players=[PlayerId.GAIA])

            available_tiles: dict[int, dict[int, bool]] = {}
            for tile in town_area.to_coords():
                available_tiles.setdefault(tile.x, {})[tile.y] = True

            for tile in castle_centered.copy().size(6).to_coords():
                available_tiles.setdefault(tile.x, {})[tile.y] = False

            # Clear the area (except trees) to make space for the towns
            for unit in units:
                tile = unit.tile
                terrain_tile = mm.get_tile(*tile)

                is_tree = unit.unit_const in trees
                is_tree_terrain = terrain_tile.terrain_id in tree_terrains or terrain_tile.layer in tree_terrains

                if not is_tree_terrain or not is_tree:
                    um.remove_unit(unit=unit)
                else:
                    available_tiles.setdefault(tile.x, {})[tile.y] = False

            self.build_random_town(scenario, available_tiles)

            # [DEBUG]
            # for x, ys in available_tiles.items():
            #     for y, v in ys.items():
            #         if not v:
            #             mm.get_tile(x, y).terrain_id = TerrainId.BLACK

    def build_random_town(self, scenario: AoE2DEScenario, available_tiles: dict[int, dict[int, bool]]) -> None:
        um = scenario.unit_manager

        xs = list(available_tiles.keys())
        ys = list(available_tiles[xs[0]].keys())

        for buildings, tries, expansion_chance in self.spawn_attempts:
            i = 0
            while i < tries:
                x, y = random.choice(xs), random.choice(ys)
                building_choice: AiBuildingDetails = random.choice(buildings)

                building, size, reservation_size = building_choice

                center = scenario.new.area().center(x, y)
                building_area = center.copy().size(size)

                # If the width or height doesn't match the wanted size, the new size was pushed out of bounds
                if building_area.get_width() != size or building_area.get_height() != size:
                    i += 1
                    continue

                tiles = center.copy().size(size).to_coords()
                if not self.is_valid_placement(available_tiles, tiles):
                    i += 1
                    continue

                self.place_building(um, building, x, y, size)
                occupied_tiles = center.copy().size(reservation_size).to_coords()

                # Chance to expand (place buildings next to current in X or Y)
                if expansion_chance < random.random():
                    self.mark_as_unavailable(available_tiles, occupied_tiles)
                    i += 1
                    continue

                # Adjacent spots in either X or Y axis
                adjacent_areas: list[tuple[int, int, Area]] = [
                    (x, y + size, building_area.copy().center(x, y + size)),
                    (x, y - size, building_area.copy().center(x, y - size)),
                    (x + size, y, building_area.copy().center(x + size, y)),
                    (x - size, y, building_area.copy().center(x - size, y)),
                ]

                for index, (x, y, adjacent) in enumerate(adjacent_areas):
                    if expansion_chance * .25 < random.random():
                        continue

                    tiles = adjacent.to_coords()

                    # If the width or height doesn't match the wanted size, the new size was pushed out of bounds
                    if adjacent.get_width() != size or adjacent.get_height() != size:
                        continue

                    if not self.is_valid_placement(available_tiles, tiles):
                        continue

                    self.place_building(um, building, x, y, size)
                    occupied_tiles.update(adjacent.copy().size(reservation_size).to_coords())

                self.mark_as_unavailable(available_tiles, occupied_tiles)

                i += 1

    def place_building(self, um: UnitManager, building: BuildingInfo, x: int, y: int, size: int) -> None:
        if size % 2 == 1:  # Is odd building size
            x, y = x + .5, y + .5

        um.add_unit(PlayerId.EIGHT, building.ID, x=x, y=y)

    def mark_as_unavailable(self, available_tiles: dict[int, dict[int, bool]], tiles: Iterable[Tile]) -> None:
        for tile in tiles:
            if tile.x not in available_tiles or tile.y not in available_tiles[tile.x]:
                continue
            available_tiles[tile.x][tile.y] = False

    def is_valid_placement(self, available_tiles: dict[int, dict[int, bool]], tiles: Iterable[Tile]) -> bool:
        for tile in tiles:
            if tile.x not in available_tiles or tile.y not in available_tiles[tile.x]:
                return False  # Unfortunately necessary as tiles outside could be trees etc.
            if not available_tiles[tile.x][tile.y]:
                return False
        return True
