from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario

from src.builders.movement_builder import MovementBuilder
from src.builders.spawner_builder import SpawnerBuilder
from src.builders.town_builder import TownBuilder
from src.data.event_data import sections
from src.data.town_data import spawn_attempts
from src.local_config import folder_de

filename = "!prepared_defend1"
scenario = AoE2DEScenario.from_file(f"{folder_de}{filename}.aoe2scenario")
tm, um, mm, xm, pm, msm = scenario.trigger_manager, scenario.unit_manager, scenario.map_manager, scenario.xs_manager, \
    scenario.player_manager, scenario.message_manager

# Create enemy towns around the edge of the map
town_builder = TownBuilder(spawn_attempts)
town_builder.apply(scenario)

# Create spawner logic in XS & Triggers for spawning the units
spawner_builder = SpawnerBuilder(sections)
spawner_builder.apply(scenario)

# ...
movement_builder = MovementBuilder()
movement_builder.apply(scenario)

scenario.write_to_file(f"{folder_de}{filename}_written.aoe2scenario")

# Seeds:
# -887778626
# 1305986759
