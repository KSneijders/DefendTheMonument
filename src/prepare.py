from random import Random

from AoE2ScenarioParser.datasets.buildings import BuildingInfo
from AoE2ScenarioParser.datasets.object_support import StartingAge
from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.terrains import TerrainId
from AoE2ScenarioParser.datasets.trigger_lists import DiplomacyState, VisibilityState
from AoE2ScenarioParser.datasets.units import UnitInfo
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario
from AoE2ScenarioRms import AoE2ScenarioRms
from AoE2ScenarioRms.flags import ObjectClear
from AoE2ScenarioRms.util import ScenarioUtil

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

asr = AoE2ScenarioRms(scenario)

# ####### UNITS ######## #

CLEAR_AREA = 15
NO_BUILD_AREA = 6

# Clear all animals, Player units and relics from the map
ScenarioUtil.clear(scenario, ObjectClear.ANIMAL_OBJECTS | ObjectClear.PLAYERS | ObjectClear.RELICS)

# Get area object for the scenario
area = scenario.new.area().select_entire_map()

center = area.copy().size(1).expand(CLEAR_AREA)
center_no_build = area.copy().select_entire_map().size(1).expand(NO_BUILD_AREA)

for unit in um.get_units_in_area(**center.to_dict(prefix='')):
    um.remove_unit(unit=unit)

center_1x1 = center.copy().size(1)
center_tile = center_1x1.corner1
center_tile_offset = center_1x1.copy().center(center_tile.x - 1, center_tile.y - 1).corner1

um.add_unit(PlayerId.GAIA, unit_const=BuildingInfo.MONUMENT.ID, tile=center_tile)

villager_spawn_distance = CLEAR_AREA * .8

center_large = center.copy().size(41).use_pattern_grid(block_size=1, gap_size=5)
coords = center_large.to_dict()

for tile in center_large.to_coords():
    for player in players:
        um.add_unit(player, unit_const=OtherInfo.MAP_REVEALER_GIANT.ID, tile=tile)

trigger = tm.add_trigger('Remove map revealers & allied vision')
for player in players:
    trigger.new_effect.remove_object(OtherInfo.MAP_REVEALER_GIANT.ID, player, **coords)

for player in players:
    for target in players:
        if player == target:
            continue
        trigger.new_effect.set_player_visibility(player, target, VisibilityState.VISIBLE)

for player in players:
    um.add_unit(player, unit_const=OtherInfo.MAP_REVEALER_GIANT.ID, tile=center_tile)
    # um.add_unit(player, unit_const=UnitInfo.HORSE_A.ID, tile=center_tile_offset)

    x = center_tile.x + (orientations[player][0] * villager_spawn_distance)
    y = center_tile.y + (orientations[player][1] * villager_spawn_distance)
    for i in range(len(orientations)):
        xoffset = orientations[i][0] / 2
        yoffset = orientations[i][1] / 2

        um.add_unit(player=player, unit_const=random_vil(), x=x + xoffset, y=y + yoffset)

# ####### PLAYERS ######## #

pm.active_players = 8

# No civ specific changes (Future?)
for player in players:
    pm.players[player].wood = 475
    pm.players[player].food = 200
    pm.players[player].gold = 100
    pm.players[player].stone = 300

    # Set starting view to Monument
    pm.players[player].initial_camera_x = center_tile.x
    pm.players[player].initial_camera_y = center_tile.y

    # Set p8 to enemy for each player
    pm.players[player].set_player_diplomacy(PlayerId.EIGHT, diplomacy=DiplomacyState.ENEMY)

pm.set_diplomacy_teams(players, diplomacy=DiplomacyState.ALLY)

# Set everyone to ENEMY for p8
pm.players[PlayerId.EIGHT].set_player_diplomacy(players, diplomacy=DiplomacyState.ENEMY)
pm.players[PlayerId.EIGHT].wood = 99999999
pm.players[PlayerId.EIGHT].food = 99999999
pm.players[PlayerId.EIGHT].gold = 99999999
pm.players[PlayerId.EIGHT].stone = 99999999
pm.players[PlayerId.EIGHT].population_cap = 1000

for player in PlayerId.all(exclude_gaia=True):
    pm.players[player].starting_age = StartingAge.DARK_AGE

# ####### TERRAIN ######## #

# Create non-buildable area around the monument (and make it look nice with some layering)
for terrain in center_no_build.to_coords(as_terrain=True):
    terrain.layer = terrain.layer if terrain.layer != -1 else terrain.terrain_id
    terrain.terrain_id = TerrainId.ROCK_1  # Non-buildable

mm.set_elevation(0, **center.copy().expand(5).to_dict(prefix=''))

# ####### ENEMY SPAWN ######## #

# area_edge = area.copy().use_only_edge(line_width=12)
# for terrain in area_edge.to_coords(as_terrain=True):
#     terrain.layer = terrain.layer if terrain.layer != -1 else terrain.terrain_id
#     terrain.terrain_id = TerrainId.ROCK_1  # Non-buildable

scenario.write_to_file(f"{folder_de}!prepared_{filename}.aoe2scenario")

militia = 0
archer = 1




