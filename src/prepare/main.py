import copy
import math
from pathlib import Path
from random import Random

from AoE2ScenarioParser.datasets.buildings import BuildingInfo
from AoE2ScenarioParser.datasets.object_support import StartingAge
from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.terrains import TerrainId
from AoE2ScenarioParser.datasets.trigger_lists import DiplomacyState, VisibilityState, Attribute, PanelLocation
from AoE2ScenarioParser.datasets.units import UnitInfo
from AoE2ScenarioParser.objects.support.tile import Tile
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario
from AoE2ScenarioRms import AoE2ScenarioRms
from AoE2ScenarioRms.debug import ApplyXsPrint
from AoE2ScenarioRms.flags import ObjectClear, ObjectMark
from AoE2ScenarioRms.util import ScenarioUtil, GridMapFactory

from src.local_config import folder_de
from src.prepare.rms import global_map_objects_config, starting_area_additional_objects_config
from src.support.values import orientations

if __name__ != '__main__':
    raise Exception('Cannot run this module through other scripts!')

players = PlayerId.all(exclude_gaia=True)
players.pop(7)

_random = Random()


def random_vil() -> int:
    return _random.choice([UnitInfo.VILLAGER_MALE.ID, UnitInfo.VILLAGER_FEMALE.ID])


################################
#     SCENARIO PREPARATION     #
################################

print("\n", "\n", "Preparation!", "\n")

TerrainId.tree_terrains()

filename = "defend1"
scenario = AoE2DEScenario.from_file(f"{folder_de}{filename}.aoe2scenario")
tm, um, mm, xm, pm, msm = scenario.trigger_manager, scenario.unit_manager, scenario.map_manager, scenario.xs_manager, \
    scenario.player_manager, scenario.message_manager

um.remove_eye_candy()

xm.initialise_xs_trigger()

# ####### UNITS ######## #

VILLAGER_SPAWN_DISTANCE = 20
VILLAGER_SPAWN_CLEAR_DISTANCE = 2
NO_BUILD_AREA = 6

# Clear all animals, Player units and relics from the map
ScenarioUtil.clear(scenario, ObjectClear.ANIMAL_OBJECTS | ObjectClear.PLAYERS | ObjectClear.RESOURCE_OBJECTS)

# Get area object for the scenario
area = scenario.new.area().select_entire_map()

center_no_build = area.copy().select_entire_map().size(0).expand(NO_BUILD_AREA)

# for unit_const in um.get_units_in_area(**center.to_dict(prefix='')):
#     um.remove_unit(unit=unit_const)

mm.set_elevation(1, **center_no_build.to_dict(prefix=''))

center_1x1 = area.copy().size(1)
center_tile = center_1x1.corner1
center_tile_offset = center_1x1.copy().center(center_tile.x - 1, center_tile.y - 1).corner1

# TODO: !!!!!!! Make NOT DELETABLE !!!!!!!
um.add_unit(PlayerId.ONE, unit_const=BuildingInfo.TEMPLE_OF_HEAVEN.ID, x=center_tile.x, y=center_tile.y)

center_large = area.copy().size(50).use_pattern_grid(block_size=1, gap_size=5)
coords = center_large.to_dict()

for tile in center_large.to_coords():
    for player in players:
        um.add_unit(player, unit_const=OtherInfo.MAP_REVEALER_GIANT.ID, tile=tile)

map_revealers_trigger = tm.add_trigger('Remove map revealers & allied vision')
for player in players:
    map_revealers_trigger.new_effect.remove_object(OtherInfo.MAP_REVEALER_GIANT.ID, player, **coords)

# Give AI full map vision
entire_map_grid = area.copy().use_pattern_grid(block_size=1, gap_size=10)
for tile in entire_map_grid.to_coords():
    um.add_unit(PlayerId.EIGHT, unit_const=OtherInfo.MAP_REVEALER_GIANT.ID, tile=tile)

# Set allied vision
for player in players:
    for target in players:
        if player == target:
            continue
        map_revealers_trigger.new_effect.set_player_visibility(player, target, VisibilityState.VISIBLE)


def get_furthest_coords(coords, n):
    if n > len(coords):
        raise ValueError("n cannot be larger than the number of coordinates")

    selected = [coords[0]]
    remaining = coords[1:]

    while len(selected) < n:
        max_min_dist = 0
        furthest = None

        for point in remaining:
            min_dist = min(
                math.hypot(abs(point.x - selected_point.x), abs(point.y - selected_point.y))
                for selected_point in selected
            )
            if min_dist > max_min_dist:
                max_min_dist = min_dist
                furthest = point
        selected.append(furthest)
        remaining.remove(furthest)

    return selected


spawnable = []
for angle in range(0, 360, 3):
    radians = math.radians(angle)
    x = math.floor(center_tile.x + VILLAGER_SPAWN_DISTANCE * math.cos(radians))
    y = math.floor(center_tile.y + VILLAGER_SPAWN_DISTANCE * math.sin(radians))

    dist = VILLAGER_SPAWN_CLEAR_DISTANCE
    units = um.get_units_in_area(x - dist, y - dist, x + dist, y + dist, players=[PlayerId.GAIA])
    units = um.filter_units_by_const([t.ID for t in OtherInfo.trees()], unit_list=units)

    if not units:
        spawnable.append(Tile(x, y))

player_start_locations = get_furthest_coords(spawnable, len(players))

disable_trigger = tm.add_trigger(f'Disable random player placements')
disable_trigger.new_condition.timer(3)
for location_index, start_location in enumerate(player_start_locations):
    um.add_unit(location_index + 1, unit_const=OtherInfo.MAP_REVEALER_GIANT.ID, tile=center_tile)

    x, y = start_location

    # Nothing works...
    # pm.players[player].initial_camera_x = math.floor(x)
    # pm.players[player].initial_camera_y = math.floor(y)
    # scenario.sections[SectionName.UNITS.value].player_data_3[player].editor_camera_x = math.floor(x)
    # scenario.sections[SectionName.UNITS.value].player_data_3[player].editor_camera_y = math.floor(y)

    # Spawn villagers
    villagers = []
    for i in range(len(orientations)):
        xoffset = orientations[i][0] / 2
        yoffset = orientations[i][1] / 2

        # Default to a player colour if randomized spawns is turned off
        villager = um.add_unit(player=location_index + 1, unit_const=random_vil(), x=x + xoffset, y=y + yoffset)
        villagers.append(villager)

    # Spawn starting resources
    starting_units_per_player = [
        (UnitInfo.JAVELINA.ID, 1),
        (UnitInfo.JAVELINA.ID, 1),
        (UnitInfo.SHEEP.ID, 8),
    ]

    sheep = []
    for unit_const, repeat in starting_units_per_player:
        while True:
            sx = (_random.random() * 8 - 4)
            sy = (_random.random() * 8 - 4)

            if max(abs(sx), abs(sy)) > 2:
                break

        orientations_copy = copy.copy(orientations)
        _random.shuffle(orientations_copy)

        for i in range(repeat):
            xoffset, yoffset = orientations_copy[i]

            fx = x + sx + (xoffset / 1.4)
            fy = y + sy + (yoffset / 1.4)

            unit = um.add_unit(
                player=PlayerId.GAIA,
                unit_const=unit_const,
                x=fx,
                y=fy,
                rotation=_random.random() * math.pi * 2
            )
            if unit_const == UnitInfo.SHEEP.ID:
                sheep.append(unit)

    # Add triggers & script for random player placement
    for target_player in players:
        trigger = tm.add_trigger(f'P{target_player} [Location {location_index}]')
        func = (
            f'bool __player_P{target_player}_spawn_location_{location_index}() {{'
            f'return (playerShuffleFinished && xsArrayGetInt(playerPositions, {location_index}) == {target_player - 1});'
            f'}}'
        )
        trigger.new_condition.script_call(func)
        trigger.new_effect.change_ownership(
            source_player=location_index + 1,
            target_player=target_player,
            selected_object_ids=[unit.reference_id for unit in villagers + sheep],
        )
        trigger.new_effect.change_view(
            quantity=0,
            source_player=target_player,
            location_x=math.floor(x),
            location_y=math.floor(y),
        )

        disable_trigger.new_effect.deactivate_trigger(trigger.trigger_id)

# ####### PLAYERS & STARTING RESOURCE (DETECTION) ######## #

pm.active_players = 8

tm.add_trigger("-- STARTING RESOURCES --").new_condition.timer(1)

default_res_check_trigger = tm.add_trigger("START RESOURCES == 'LOW'?")
default_res_check_trigger.new_condition.accumulate_attribute(quantity=1, attribute=Attribute.FOOD_STORAGE,
                                                             source_player=PlayerId.ONE)
default_res_check_trigger.new_condition.or_()
default_res_check_trigger.new_condition.accumulate_attribute(quantity=1, attribute=Attribute.WOOD_STORAGE,
                                                             source_player=PlayerId.ONE)

# Create trigger to set everyone to default RES
set_start_res_trigger = tm.add_trigger('SET DEFAULT START RESOURCES')
set_start_res_trigger.new_condition.timer(1)
message = ("      STARTING RESOURCES WERE NOT SET TO 'LOW'!\n \n"
           "                    Defaulting everyone to base resource.\n"
           "This will be incorrect for some civs, a restart is recommended.")
set_start_res_trigger.new_effect.deactivate_trigger(default_res_check_trigger.trigger_id)
set_start_res_trigger.new_effect.display_instructions(instruction_panel_position=PanelLocation.TOP, message=message)

# Create trigger to add TC resources to everyone
add_tc_res_trigger = tm.add_trigger('ADD TC RESOURCES', enabled=False)

default_res_check_trigger.new_effect.deactivate_trigger(set_start_res_trigger.trigger_id)
default_res_check_trigger.new_effect.activate_trigger(add_tc_res_trigger.trigger_id)

for player in players:
    pm.players[player].wood = 0
    pm.players[player].food = 0
    pm.players[player].gold = 0
    pm.players[player].stone = 0

    # Set starting view to Monument
    pm.players[player].initial_camera_x = center_tile.x
    pm.players[player].initial_camera_y = center_tile.y

    # Set p8 to enemy for each player
    pm.players[player].set_player_diplomacy(PlayerId.EIGHT, diplomacy=DiplomacyState.ENEMY)

    add_tc_res_trigger.new_effect.tribute(-275, Attribute.WOOD_STORAGE, player, PlayerId.GAIA)
    add_tc_res_trigger.new_effect.tribute(-100, Attribute.STONE_STORAGE, player, PlayerId.GAIA)

    set_start_res_trigger.new_effect.tribute(-475, Attribute.WOOD_STORAGE, player, PlayerId.GAIA)
    set_start_res_trigger.new_effect.tribute(-200, Attribute.FOOD_STORAGE, player, PlayerId.GAIA)
    set_start_res_trigger.new_effect.tribute(-100, Attribute.GOLD_STORAGE, player, PlayerId.GAIA)
    set_start_res_trigger.new_effect.tribute(-300, Attribute.STONE_STORAGE, player, PlayerId.GAIA)

pm.set_diplomacy_teams(players, diplomacy=DiplomacyState.ALLY)

# Set everyone to ENEMY for p8
pm.players[PlayerId.EIGHT].set_player_diplomacy(players, diplomacy=DiplomacyState.ENEMY)

resources = [
    Attribute.WOOD_STORAGE,
    Attribute.FOOD_STORAGE,
    Attribute.GOLD_STORAGE,
    Attribute.STONE_STORAGE,
]

for resource in resources:
    name = resource.name.split('_')[0]

    map_revealers_trigger = tm.add_trigger(f"GIVE P8 {name}", looping=True)
    map_revealers_trigger.new_condition.accumulate_attribute(quantity=100_000, attribute=resource,
                                                             source_player=PlayerId.EIGHT, inverted=True)
    map_revealers_trigger.new_effect.tribute(-200_000, resource, PlayerId.EIGHT, PlayerId.GAIA)

pm.players[PlayerId.EIGHT].population_cap = 1000

for player in PlayerId.all(exclude_gaia=True):
    pm.players[player].starting_age = StartingAge.DARK_AGE

# ####### TERRAIN ######## #

# Create non-buildable area around the monument (and make it look nice with some layering)
for terrain in center_no_build.to_coords(as_terrain=True):
    terrain.layer = terrain.layer if terrain.layer != -1 else terrain.terrain_id
    terrain.terrain_id = TerrainId.ROCK_1  # Non-buildable

# ####### RANDOM RESOURCE SPAWNING ######## #

asr = AoE2ScenarioRms(scenario)

# Starting deer
grid_map = GridMapFactory.block(
    scenario=scenario,
    object_marks=ObjectMark.TREES | ObjectMark.CLIFFS,
    area=scenario.new.area().select_entire_map().use_only_edge(
        line_width=math.floor((scenario.map_manager.map_size / 2) - (VILLAGER_SPAWN_DISTANCE + 1)))
)
asr.create_objects(starting_area_additional_objects_config, grid_map)

# Global resources
grid_map = GridMapFactory.block(
    scenario=scenario,
    object_marks=ObjectMark.TREES | ObjectMark.CLIFFS,
    area=scenario.new.area().select_entire_map().use_only_edge(line_width=math.ceil(scenario.map_manager.map_size / 8))
)
asr.create_objects(global_map_objects_config, grid_map)

ApplyXsPrint(asr)

# Add the conditional logic for random player placement
random_players_file_path = Path(__file__).parent / 'xs' / 'random_players.xs'
xm.add_script(xs_file_path=str(random_players_file_path))

scenario.write_to_file(f"{folder_de}!prepared_{filename}.aoe2scenario")
