import math

from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.scenarios.aoe2_scenario import AoE2Scenario


class MovementBuilder:
    def __init__(self):
        pass

    def apply(self, scenario: AoE2Scenario) -> None:
        tm = scenario.trigger_manager

        map_size = scenario.map_manager.map_size
        trigger = tm.add_trigger('Movement loop', looping=True)
        trigger.new_condition.timer(60)

        block_size = 13
        for x in range(0, map_size, block_size):
            for y in range(0, map_size, block_size):
                trigger.new_effect.attack_move(
                    source_player=PlayerId.EIGHT,
                    location_x=math.floor(map_size / 2),
                    location_y=math.floor(map_size / 2),
                    area_x1=x,
                    area_y1=y,
                    area_x2=min(map_size, x + block_size - 1),
                    area_y2=min(map_size, y + block_size - 1),
                )
