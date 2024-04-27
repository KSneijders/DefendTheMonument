from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.units import UnitInfo
from AoE2ScenarioRms.enums import GroupingMethod
from AoE2ScenarioRms.rms import CreateObjectConfig

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