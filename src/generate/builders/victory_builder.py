from AoE2ScenarioParser.datasets.buildings import BuildingInfo
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario


class VictoryBuilder:
    def __init__(self):
        ...

    def apply(self, scenario: AoE2DEScenario):
        um, tm = scenario.unit_manager, scenario.trigger_manager

        targets = um.filter_units_by_const(unit_consts=[BuildingInfo.TEMPLE_OF_HEAVEN.ID], player_list=[PlayerId.ONE])
        target = targets[0]

        trigger = tm.add_trigger("Lose TEMPLE OF HEAVEN")
        trigger.new_condition.destroy_object(unit_object=target.reference_id)
        trigger.new_effect.declare_victory(source_player=PlayerId.EIGHT)
