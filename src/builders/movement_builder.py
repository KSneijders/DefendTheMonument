import math

from AoE2ScenarioParser.datasets.buildings import BuildingInfo
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.objects.data_objects.unit import Unit
from AoE2ScenarioParser.scenarios.aoe2_scenario import AoE2Scenario

CLOSE_TARGET_AREA = 20


class MovementBuilder:
    def __init__(self):
        pass

    def apply(self, scenario: AoE2Scenario) -> None:
        um = scenario.unit_manager

        targets = um.filter_units_by_const(unit_consts=[BuildingInfo.TEMPLE_OF_HEAVEN.ID], player_list=[PlayerId.ONE])
        target = targets[0]

        # self._map_movement_loop(scenario, target)
        self._close_movement_loop(scenario, target)

    def _map_movement_loop(self, scenario: AoE2Scenario, target: Unit) -> None:
        tm = scenario.trigger_manager

        map_size = scenario.map_manager.map_size
        trigger = tm.add_trigger('Movement loop', looping=True)
        trigger.new_condition.timer(10)

        block_size = 25
        for x in range(0, map_size, block_size):
            for y in range(0, map_size, block_size):
                trigger.new_effect.attack_move(
                    source_player=PlayerId.EIGHT,
                    location_x=math.floor(target.x),
                    location_y=math.floor(target.y),
                    area_x1=x,
                    area_y1=y,
                    area_x2=min(map_size, x + block_size - 1),
                    area_y2=min(map_size, y + block_size - 1),
                )

    def _close_movement_loop(self, scenario: AoE2Scenario, target: Unit) -> None:
        tm = scenario.trigger_manager

        center_area = scenario.new.area().size(CLOSE_TARGET_AREA)

        trigger = tm.add_trigger('Close movement loop', looping=True)
        trigger.new_condition.timer(30)
        trigger.new_effect.task_object(
            source_player=PlayerId.EIGHT,
            location_object_reference=target.reference_id,
            **center_area.to_dict()
        )
