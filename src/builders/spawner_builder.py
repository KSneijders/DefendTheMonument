from pathlib import Path

from AoE2ScenarioParser.datasets.buildings import BuildingInfo
from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.techs import TechInfo
from AoE2ScenarioParser.datasets.units import UnitInfo
from AoE2ScenarioParser.helper.pretty_format import pretty_format_name, pretty_format_dict
from AoE2ScenarioParser.objects.data_objects.trigger import Trigger
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario

from src.events.events import Event, Create, Research, ResearchDependency
from src.support.time import Time
from src.types.types import SectionType


class SpawnerBuilder:
    def __init__(self, sections: SectionType):
        self.sections: SectionType = sections

        self.timeline: dict[int, list[Event]] = {}
        self.research_times: dict[int, int] = {}
        self.unit_spawn_times: dict[int, list[tuple[int, int]]] = {}

        self.units: set[tuple[UnitInfo, BuildingInfo]] = set()
        self.units_by_building: dict[BuildingInfo, set[UnitInfo]] = {}

        self._initialize()

    def apply(self, scenario: AoE2DEScenario) -> None:
        tm, um, xm = scenario.trigger_manager, scenario.unit_manager, scenario.xs_manager
        xm.initialise_xs_trigger()

        # Remove TC from the buildings
        self.sections.pop(BuildingInfo.TOWN_CENTER)

        init_trigger = tm.add_trigger('Initialize spawn loops')
        init_trigger.new_condition.timer(timer=3)

        xs_init = []
        xs_arrays_init = []
        xs_fill_arrays = []

        number_of_buildings = len(self.sections)
        number_of_units = len(self.units)

        xs_arrays_init.extend([
            'int BUILDING_COUNTS = -1;               // The amount of buildings',
            'int BUILDINGS_ALIVE_STATE_ARRAYS = -1;  // Building alive state',
            'int BUILDINGS_ALIVE_IDX_ARRAYS = -1;    // What Idx are in alive state',
            'int UNIT_QUEUE_ARRAY = -1;              // The amount of units to be queued',
            'int UNIT_SPAWN_CHANCE_ARRAY = -1;       // The chance of adding a unit each second (in %)',
        ])

        xs_fill_arrays.extend([f'int temp = 0;', ''])

        # Add unit constants
        for unit_idx, (unit, building) in enumerate(self.units):
            xs_init.append(f'int {unit.name} = {unit_idx};')
        xs_init.append('')  # Separating newline

        # Add building constants
        for building_idx, (building, sections) in enumerate(self.sections.items()):
            xs_init.append(f'int {building.name} = {building_idx};')

            if building in [BuildingInfo.BLACKSMITH, BuildingInfo.UNIVERSITY]:
                continue

            gens = um.filter_units_by_const([building.ID], player_list=[PlayerId.EIGHT])
            number_of_gens = len(gens)

            if number_of_gens == 0:
                continue

            xs_fill_arrays.append(f'// {building.name}')
            xs_fill_arrays.append(f'xsArraySetInt(BUILDING_COUNTS, {building_idx}, {number_of_gens});')
            xs_fill_arrays.append(
                f'temp = xsArrayCreateBool({number_of_gens}, true, "__buildings_alive_state_arrays_{building.name}_532465895");')
            xs_fill_arrays.append(f'xsArraySetInt(BUILDINGS_ALIVE_STATE_ARRAYS, {building_idx}, temp);')

            xs_fill_arrays.append(
                f'temp = xsArrayCreateInt({number_of_gens}, 0, "__buildings_alive_idx_arrays_{building.name}_485602375");')
            xs_fill_arrays.extend([
                f'for (i = 0; < {number_of_gens}) {{',
                f'    xsArraySetInt(temp, i, i);',
                f'}}',
            ])

            initial_cycle: dict[UnitInfo, Trigger] = {}
            previous_cycle: dict[UnitInfo, Trigger] = {}

            initial_spawn: dict[UnitInfo, Trigger] = {}
            previous_spawn: dict[UnitInfo, Trigger] = {}

            for gen_idx, gen in enumerate(gens):
                for index, unit in enumerate(self.units_by_building[building]):
                    cycle_name = f'[C{gen_idx}] {building.name} {unit.name}'
                    spawn_name = f'[S{gen_idx}] {building.name} {unit.name}'

                    cycle_trigger = tm.add_trigger(name=cycle_name, enabled=False)
                    spawn_trigger = tm.add_trigger(name=spawn_name, enabled=False)

                    # First iteration, save trigger for last iteration
                    if gen_idx == 0:
                        initial_cycle[unit] = cycle_trigger
                        initial_spawn[unit] = spawn_trigger

                    # Active same level spawn trigger
                    cycle_trigger.new_condition.timer(2)  # timer(1) doesn't work in the game [rate limit = 30]
                    cycle_trigger.new_effect.activate_trigger(spawn_trigger.trigger_id)

                    # if building == BuildingInfo.BARRACKS:
                    #     cycle_trigger.new_effect.display_instructions(message=f'{gen_idx}', display_time=1)

                    func = (
                        f'bool __try_spawn_{unit.name}_{building.name}{gen_idx}() {{'
                        f'return (trainUnitCondition({unit.name}));'
                        f'}}'
                    )
                    spawn_trigger.new_condition.script_call(xs_function=func)
                    spawn_trigger.new_effect.train_unit(
                        quantity=1,
                        object_list_unit_id=unit.ID,
                        source_player=PlayerId.EIGHT,
                        selected_object_ids=gen.reference_id,
                    )

                    # Deactivate previous spawn trigger
                    if unit in previous_spawn:
                        cycle_trigger.new_effect.deactivate_trigger(previous_spawn[unit].trigger_id)

                    # Create chain activations start -> end
                    if unit in previous_cycle:
                        previous_cycle[unit].new_effect.activate_trigger(cycle_trigger.trigger_id)

                    # Last iteration
                    if gen_idx == len(gens) - 1:
                        initial_cycle[unit].new_effect.deactivate_trigger(spawn_trigger.trigger_id)
                        # Swap the final 2 entries around for consistency with the other triggers
                        (
                            initial_cycle[unit].effects[-2],
                            initial_cycle[unit].effects[-1],
                        ) = (
                            initial_cycle[unit].effects[-1],
                            initial_cycle[unit].effects[-2],
                        )

                        cycle_trigger.new_effect.activate_trigger(initial_cycle[unit].trigger_id)
                    else:
                        previous_cycle[unit] = cycle_trigger
                        previous_spawn[unit] = spawn_trigger

            for trigger in initial_cycle.values():
                init_trigger.new_effect.activate_trigger(trigger.trigger_id)

            # Run over gens again, nicely ordered triggers
            for gen_idx, gen in enumerate(gens):
                gen_lost_trigger = tm.add_trigger(f'[{building.name} {gen_idx}] Destroyed')
                gen_lost_trigger.new_condition.destroy_object(unit_object=gen.reference_id)

                func = (
                    f'void __on_{building.name}_{gen_idx}_lost() {{'
                    f'buildingDestroyed({building_idx}, {gen_idx});'
                    f'}}'
                )
                gen_lost_trigger.new_effect.script_call(message=func)

            xs_fill_arrays.append(f'xsArraySetInt(BUILDINGS_ALIVE_IDX_ARRAYS, {building_idx}, temp);\n')

        xm.add_script(xs_string='\n'.join(xs_init))
        xm.add_script(xs_string='\n'.join(xs_arrays_init))
        xm.add_script(xs_string='\n'.join([
            f'rule main_spawner_initialise__065238954',
            f'    active',
            f'    runImmediately',
            f'    minInterval 1',
            f'    maxInterval 1',
            f'    priority 999',
            f'{{',
            *[f'    {string}' for string in [
                f'BUILDING_COUNTS = xsArrayCreateInt({number_of_buildings}, 0, "__num_of_buildings_345976581");',
                f'BUILDINGS_ALIVE_STATE_ARRAYS = xsArrayCreateInt({number_of_buildings}, 0, "__buildings_alive_state_arrays_264854169");',
                f'BUILDINGS_ALIVE_IDX_ARRAYS = xsArrayCreateInt({number_of_buildings}, 0, "__buildings_alive_idx_arrays_485721650");',
                f'UNIT_QUEUE_ARRAY = xsArrayCreateInt({number_of_units}, 0, "__unit_queue_548002659");',
                f'UNIT_SPAWN_CHANCE_ARRAY = xsArrayCreateInt({number_of_units}, 0, "__unit_spawn_chance_array_346179758");',
                f'',
                *xs_fill_arrays,
                f'xsDisableSelf();',
                f'xsEnableRule("main_spawn_loop__456879123");'
            ]],
            f'}}',
        ]))

        functions_file = Path(__file__).parent.parent / 'xs' / 'functions.xs'
        xm.add_script(xs_file_path=str(functions_file.absolute()))

        xm.add_script(xs_string='\n'.join([
            f'rule main_spawn_loop__456879123',
            f'    inactive',
            f'    runImmediately',
            f'    minInterval 1',
            f'    maxInterval 1',
            f'    priority 999',
            f'{{',
            f'    // Currently does NOT support adding more than one unit per second',
            f'    for (i = 0; < {number_of_units}) {{',
            f'        if (shouldSpawn(i)) {{',
            f'            increaseUnitQueue(i, 1);',
            f'        }}',
            f'    }}',
            f'}}',
        ]))

        for research, time in self.research_times.items():
            tech = TechInfo.from_id(research)
            name = pretty_format_name(tech.name)

            trigger = tm.add_trigger(f'Research {name} @ {time}')
            trigger.new_condition.timer(time)
            trigger.new_effect.research_technology(PlayerId.EIGHT, technology=tech.ID)

            if tech in (TechInfo.FEUDAL_AGE, TechInfo.CASTLE_AGE, TechInfo.IMPERIAL_AGE):
                trigger.new_effect.display_instructions(OtherInfo.SIGN.ID, PlayerId.EIGHT, message=f"<ORANGE>Player 8 reached the {name}!")

        for unit, spawns in self.unit_spawn_times.items():
            unit = UnitInfo.from_id(unit)
            name = unit.name.lower()

            for (time, rate) in spawns:
                trigger = tm.add_trigger(f'Spawn {rate} {name}/min @ {time}')
                trigger.new_condition.timer(time)

                func = (
                    f'void __spawn_{rate}_{name}_at_{time}() {{'
                    f'xsArraySetInt(UNIT_SPAWN_CHANCE_ARRAY, {unit.name}, {rate});'
                    f'}}'
                )

                trigger.new_effect.script_call(message=func)

    def _initialize(self):
        research_times: dict[int, int] = {}
        unit_spawn_times: dict[int, list[tuple[int, int]]] = {}
        timeline: dict[int, list[Event]] = {}

        for building_sections in self.sections.values():
            for section in building_sections:
                dependency_time_offset = 0

                for event in section:
                    if isinstance(event, Research):
                        time = Time.to_seconds(event.time)
                        research_times[event.tech.ID] = time + dependency_time_offset
                    elif isinstance(event, Create):
                        time = Time.to_seconds(event.time)
                        unit_spawn_times.setdefault(event.unit.ID, []).append((time + dependency_time_offset, event.rate))
                    elif isinstance(event, ResearchDependency):
                        if event.tech.ID not in research_times:
                            raise ValueError(f'Research dependency not found for {event.tech}')

                        time = research_times[event.tech.ID]
                        dependency_time_offset = time
                        continue
                    else:
                        raise ValueError(f'Invalid event type: {event}')

                    timeline.setdefault(time + dependency_time_offset, []).append(event)

        self.timeline = timeline
        self.research_times = research_times
        self.unit_spawn_times = unit_spawn_times

        units: set[tuple[UnitInfo, BuildingInfo]] = set()
        units_by_building: dict[BuildingInfo, set[UnitInfo]] = {}

        for building, building_events in self.sections.items():
            for unit_events in building_events:
                for event in unit_events:
                    if isinstance(event, Create):
                        units.add((event.unit, building))
                        units_by_building.setdefault(building, set()).add(event.unit)

        self.units = units
        self.units_by_building = units_by_building

    def print(self):
        sorted_times = sorted(self.timeline.keys())
        for time in sorted_times:
            print(f"> Time {Time.from_seconds(time)}")

            researches, creations = [], []
            for event in self.timeline[time]:
                if isinstance(event, Research):
                    researches.append(event)
                elif isinstance(event, Create):
                    creations.append(event)

            for research in researches:
                print(f"    {research}")
            for creation in creations:
                print(f"    {creation}")
