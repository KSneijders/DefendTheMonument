import copy
import math
from random import Random

from AoE2ScenarioParser.datasets.buildings import BuildingInfo
from AoE2ScenarioParser.datasets.object_support import StartingAge
from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.terrains import TerrainId
from AoE2ScenarioParser.datasets.trigger_lists import DiplomacyState, VisibilityState, Attribute, PanelLocation
from AoE2ScenarioParser.datasets.units import UnitInfo
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario
from AoE2ScenarioParser.sections.aoe2_file_section import SectionName
from AoE2ScenarioRms import AoE2ScenarioRms
from AoE2ScenarioRms.debug import ApplyBlockedAsBlack, ApplyXsPrint
from AoE2ScenarioRms.debug.apply_state_as_black import ApplyStateAsBlack
from AoE2ScenarioRms.enums import GroupingMethod
from AoE2ScenarioRms.flags import ObjectClear, TerrainMark, ObjectMark
from AoE2ScenarioRms.rms import CreateObjectConfig
from AoE2ScenarioRms.util import ScenarioUtil, GridMapFactory

from local_config import folder_de
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


filename = "defend1"
scenario = AoE2DEScenario.from_file(f"{folder_de}{filename}.aoe2scenario")
tm, um, mm, xm, pm, msm = scenario.trigger_manager, scenario.unit_manager, scenario.map_manager, scenario.xs_manager, \
    scenario.player_manager, scenario.message_manager

# ####### UNITS ######## #

CLEAR_AREA = 24
NO_BUILD_AREA = 6

# Clear all animals, Player units and relics from the map
ScenarioUtil.clear(scenario, ObjectClear.ANIMAL_OBJECTS | ObjectClear.PLAYERS | ObjectClear.RESOURCE_OBJECTS)

# Get area object for the scenario
area = scenario.new.area().select_entire_map()

center = area.copy().size(1).expand(CLEAR_AREA)
center_no_build = area.copy().select_entire_map().size(0).expand(NO_BUILD_AREA)

for unit in um.get_units_in_area(**center.to_dict(prefix='')):
    um.remove_unit(unit=unit)

center_1x1 = center.copy().size(1)
center_tile = center_1x1.corner1
center_tile_offset = center_1x1.copy().center(center_tile.x - 1, center_tile.y - 1).corner1

# TODO: !!!!!!! Make NOT DELETABLE !!!!!!!
um.add_unit(PlayerId.ONE, unit_const=BuildingInfo.TEMPLE_OF_HEAVEN.ID, x=center_tile.x, y=center_tile.y)

villager_spawn_distance = CLEAR_AREA * .8

center_large = center.copy().size(50).use_pattern_grid(block_size=1, gap_size=5)
coords = center_large.to_dict()

for tile in center_large.to_coords():
    for player in players:
        um.add_unit(player, unit_const=OtherInfo.MAP_REVEALER_GIANT.ID, tile=tile)

map_revealers_trigger = tm.add_trigger('Remove map revealers & allied vision')
for player in players:
    map_revealers_trigger.new_effect.remove_object(OtherInfo.MAP_REVEALER_GIANT.ID, player, **coords)


for player in players:
    for target in players:
        if player == target:
            continue
        map_revealers_trigger.new_effect.set_player_visibility(player, target, VisibilityState.VISIBLE)

change_view_trigger = tm.add_trigger('Change view trigger')
for player in players:
    um.add_unit(player, unit_const=OtherInfo.MAP_REVEALER_GIANT.ID, tile=center_tile)

    x = center_tile.x + (orientations[player][0] * villager_spawn_distance)
    y = center_tile.y + (orientations[player][1] * villager_spawn_distance)

    # Nothing works...
    # pm.players[player].initial_camera_x = math.floor(x)
    # pm.players[player].initial_camera_y = math.floor(y)
    # scenario.sections[SectionName.UNITS.value].player_data_3[player].editor_camera_x = math.floor(x)
    # scenario.sections[SectionName.UNITS.value].player_data_3[player].editor_camera_y = math.floor(y)

    change_view_trigger.new_effect.change_view(
        quantity=0,
        source_player=player,
        location_x=math.floor(x),
        location_y=math.floor(y),
    )

    for i in range(len(orientations)):
        xoffset = orientations[i][0] / 2
        yoffset = orientations[i][1] / 2

        um.add_unit(player=player, unit_const=random_vil(), x=x + xoffset, y=y + yoffset)

    # Spawn starting boars
    starting_units_per_player = [
        (UnitInfo.JAVELINA.ID, 1, PlayerId.GAIA),
        (UnitInfo.JAVELINA.ID, 1, PlayerId.GAIA),
        (UnitInfo.SHEEP.ID, 8, None),
    ]

    for unit, repeat, target_player in starting_units_per_player:
        if target_player is None:
            target_player = player

        while True:
            sx = (_random.random() * 10 - 5)
            sy = (_random.random() * 10 - 5)

            if max(abs(sx), abs(sy)) > 2:
                break

        orientations_copy = copy.copy(orientations)
        _random.shuffle(orientations_copy)

        for i in range(repeat):
            xoffset, yoffset = orientations_copy[i]

            fx = x + sx + (xoffset / 1.4)
            fy = y + sy + (yoffset / 1.4)

            um.add_unit(player=target_player, unit_const=unit, x=fx, y=fy, rotation=_random.random() * math.pi * 2)

# ####### PLAYERS & STARTING RESOURCE (DETECTION) ######## #

pm.active_players = 8

tm.add_trigger("-- STARTING RESOURCES --").new_condition.timer(1)

default_res_check_trigger = tm.add_trigger("START RESOURCES == 'LOW'?")
default_res_check_trigger.new_condition.accumulate_attribute(quantity=1, attribute=Attribute.FOOD_STORAGE, source_player=PlayerId.ONE)
default_res_check_trigger.new_condition.or_()
default_res_check_trigger.new_condition.accumulate_attribute(quantity=1, attribute=Attribute.WOOD_STORAGE, source_player=PlayerId.ONE)

# Create trigger to set everyone to default RES
set_start_res_trigger = tm.add_trigger('SET DEFAULT START RESOURCES')
set_start_res_trigger.new_condition.timer(1)
message = ("      STARTING RESOURCES WERE NOT SET TO 'LOW'!\n \n"
           "                    Defaulting everyone to base resource.\n"
           "This will be incorrect for some civs, a restart is recommended.")
set_start_res_trigger.new_effect.deactivate_trigger(default_res_check_trigger.trigger_id)
set_start_res_trigger.new_effect.display_instructions(instruction_panel_position=PanelLocation.CENTER, message=message)

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
    map_revealers_trigger.new_condition.accumulate_attribute(quantity=100_000, attribute=resource, source_player=PlayerId.EIGHT, inverted=True)
    map_revealers_trigger.new_effect.tribute(-200_000, resource, PlayerId.EIGHT, PlayerId.GAIA)

pm.players[PlayerId.EIGHT].population_cap = 1000

for player in PlayerId.all(exclude_gaia=True):
    pm.players[player].starting_age = StartingAge.DARK_AGE

# ####### TERRAIN ######## #

# Create non-buildable area around the monument (and make it look nice with some layering)
for terrain in center_no_build.to_coords(as_terrain=True):
    terrain.layer = terrain.layer if terrain.layer != -1 else terrain.terrain_id
    terrain.terrain_id = TerrainId.ROCK_1  # Non-buildable

mm.set_elevation(0, **center.copy().expand(10).to_dict(prefix=''))

# ####### RANDOM RESOURCE SPAWNING ######## #

grid_map = GridMapFactory.block(
    scenario=scenario,
    object_marks=ObjectMark.TREES | ObjectMark.CLIFFS,
    area=scenario.new.area().select_entire_map().use_only_edge(line_width=math.ceil(scenario.map_manager.map_size / 8))
)

create_objects_config: list[CreateObjectConfig] = [
    CreateObjectConfig(
        name='gold',
        const=OtherInfo.GOLD_MINE.ID,
        grouping=GroupingMethod.TIGHT,
        number_of_objects=(4, 6),
        temp_min_distance_group_placement=14,
        min_distance_group_placement=4,
        _max_potential_group_count=150,
    ),
    CreateObjectConfig(
        name='stone',
        const=OtherInfo.STONE_MINE.ID,
        grouping=GroupingMethod.TIGHT,
        number_of_objects=(3, 4),
        temp_min_distance_group_placement=16,
        min_distance_group_placement=4,
        _max_potential_group_count=150,
    ),
    CreateObjectConfig(
        name='berries',
        const=OtherInfo.FORAGE_BUSH.ID,
        grouping=GroupingMethod.TIGHT,
        number_of_objects=(5, 6),
        temp_min_distance_group_placement=22,
        min_distance_group_placement=5,
        _max_potential_group_count=60,
    ),
    CreateObjectConfig(
        name='deer',
        const=UnitInfo.DEER.ID,
        grouping=GroupingMethod.LOOSE,
        number_of_objects=(3, 4),
        temp_min_distance_group_placement=20,
        min_distance_group_placement=3,
        _max_potential_group_count=60,
    ),
    CreateObjectConfig(
        name='relic',
        const=OtherInfo.RELIC.ID,
        number_of_objects=1,
        temp_min_distance_group_placement=26,
        min_distance_group_placement=1,
        _max_potential_group_count=20,
    ),
]

asr = AoE2ScenarioRms(scenario)
asr.create_objects(create_objects_config, grid_map)

ApplyXsPrint(asr)

scenario.write_to_file(f"{folder_de}!prepared_{filename}.aoe2scenario")
