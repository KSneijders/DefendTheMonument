from AoE2ScenarioParser.datasets.techs import TechInfo
from AoE2ScenarioParser.datasets.units import UnitInfo

from src.generate.events.events import Event, Research, ResearchDependency, Create

archery_range_techs: list[Event] = [
    # @formatter:off
    ResearchDependency(TechInfo.CASTLE_AGE),

    Research(TechInfo.THUMB_RING,       time='09:00'),

    ResearchDependency(TechInfo.IMPERIAL_AGE),

    Research(TechInfo.PARTHIAN_TACTICS, time='08:00'),
    # @formatter:on
]

archer_line: list[Event] = [
    # @formatter:off
    ResearchDependency(TechInfo.FEUDAL_AGE),
    Create(UnitInfo.ARCHER,        time='00:00', rate=2),
    Create(UnitInfo.ARCHER,        time='02:00', rate=4),
    Create(UnitInfo.ARCHER,        time='04:00', rate=6),
    Create(UnitInfo.ARCHER,        time='10:00', rate=9),

    ResearchDependency(TechInfo.CASTLE_AGE),
    Create(UnitInfo.ARCHER,        time='00:00', rate=10),
    Research(TechInfo.CROSSBOWMAN, time='01:30'),
    Create(UnitInfo.ARCHER,        time='04:00', rate=12),
    Create(UnitInfo.ARCHER,        time='07:00', rate=15),

    ResearchDependency(TechInfo.IMPERIAL_AGE),
    Research(TechInfo.ARBALESTER,  time='02:00'),
    # @formatter:on
]

skirmisher_line: list[Event] = [
    # @formatter:off
    ResearchDependency(TechInfo.FEUDAL_AGE),
    Create(UnitInfo.SKIRMISHER,            time='00:00', rate=3),
    Create(UnitInfo.SKIRMISHER,            time='05:00', rate=6),
    Create(UnitInfo.SKIRMISHER,            time='10:00', rate=9),

    ResearchDependency(TechInfo.CASTLE_AGE),
    Research(TechInfo.ELITE_SKIRMISHER,    time='05:00'),
    Create(UnitInfo.SKIRMISHER,            time='08:00', rate=12),

    ResearchDependency(TechInfo.IMPERIAL_AGE),
    Research(TechInfo.IMPERIAL_SKIRMISHER, time='12:00'),
    # @formatter:on
]

cavalry_archer_line: list[Event] = [
    # @formatter:off
    ResearchDependency(TechInfo.CASTLE_AGE),
    Create(UnitInfo.CAVALRY_ARCHER,         time='00:00', rate=1),
    Create(UnitInfo.CAVALRY_ARCHER,         time='02:00', rate=3),
    Create(UnitInfo.CAVALRY_ARCHER,         time='05:00', rate=6),
    Create(UnitInfo.CAVALRY_ARCHER,         time='12:00', rate=8),

    ResearchDependency(TechInfo.IMPERIAL_AGE),
    Create(UnitInfo.CAVALRY_ARCHER,         time='03:00', rate=10),
    Create(UnitInfo.CAVALRY_ARCHER,         time='08:00', rate=12),
    Research(TechInfo.HEAVY_CAVALRY_ARCHER, time='13:00'),

    # @formatter:on
]

elephant_archer_line: list[Event] = [
    # @formatter:off
    ResearchDependency(TechInfo.CASTLE_AGE),
    Create(UnitInfo.ELEPHANT_ARCHER,         time='00:00', rate=1),
    Create(UnitInfo.ELEPHANT_ARCHER,         time='02:00', rate=2),
    Create(UnitInfo.ELEPHANT_ARCHER,         time='05:00', rate=4),
    Create(UnitInfo.ELEPHANT_ARCHER,         time='08:00', rate=5),
    Create(UnitInfo.ELEPHANT_ARCHER,         time='16:00', rate=6),

    ResearchDependency(TechInfo.IMPERIAL_AGE),
    Create(UnitInfo.ELEPHANT_ARCHER,         time='00:00', rate=8),
    Create(UnitInfo.ELEPHANT_ARCHER,         time='10:00', rate=10),
    Research(TechInfo.ELITE_ELEPHANT_ARCHER, time='16:00'),
    # @formatter:on
]

hand_cannoneer_line: list[Event] = [
    # @formatter:off
    ResearchDependency(TechInfo.CHEMISTRY),
    Create(UnitInfo.HAND_CANNONEER, time='00:00', rate=2),
    Create(UnitInfo.HAND_CANNONEER, time='08:00', rate=4),
    Create(UnitInfo.HAND_CANNONEER, time='12:00', rate=8),
    Create(UnitInfo.HAND_CANNONEER, time='18:00', rate=12),
    # @formatter:on
]

genitour_line: list[Event] = [
    # @formatter:off
    ResearchDependency(TechInfo.CASTLE_AGE),
    Create(UnitInfo.GENITOUR,         time='03:00', rate=2),
    Create(UnitInfo.GENITOUR,         time='09:00', rate=6),
    Create(UnitInfo.GENITOUR,         time='17:00', rate=9),

    ResearchDependency(TechInfo.IMPERIAL_AGE),
    Create(UnitInfo.GENITOUR,         time='06:00', rate=12),
    Research(TechInfo.ELITE_GENITOUR, time='06:00'),
    # @formatter:on
]