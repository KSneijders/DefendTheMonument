from AoE2ScenarioParser.datasets.techs import TechInfo
from AoE2ScenarioParser.datasets.units import UnitInfo

from src.implement.events.events import Research, ResearchDependency, Create, Event

stable_techs: list[Event] = [
    # @formatter:off
    ResearchDependency(TechInfo.FEUDAL_AGE),

    Research(TechInfo.BLOODLINES,       time='08:00'),

    ResearchDependency(TechInfo.CASTLE_AGE),

    Research(TechInfo.HUSBANDRY,        time='03:00'),
    # @formatter:on
]

scout_line: list[Event] = [
    # @formatter:off
    ResearchDependency(TechInfo.FEUDAL_AGE),
    Create(UnitInfo.SCOUT_CAVALRY,   time='00:00', rate=1),
    Create(UnitInfo.SCOUT_CAVALRY,   time='02:00', rate=3),
    Create(UnitInfo.SCOUT_CAVALRY,   time='05:00', rate=8),

    ResearchDependency(TechInfo.CASTLE_AGE),
    Research(TechInfo.LIGHT_CAVALRY, time='02:30'),
    Create(UnitInfo.SCOUT_CAVALRY,   time='10:00', rate=12),

    ResearchDependency(TechInfo.IMPERIAL_AGE),
    Create(UnitInfo.SCOUT_CAVALRY,   time='04:00', rate=15),
    Research(TechInfo.HUSSAR,        time='06:00'),
    # @formatter:on
]

knight_line: list[Event] = [
    # @formatter:off
    ResearchDependency(TechInfo.CASTLE_AGE),
    Create(UnitInfo.KNIGHT,     time='00:00', rate=2),
    Create(UnitInfo.KNIGHT,     time='11:00', rate=4),
    Create(UnitInfo.KNIGHT,     time='20:00', rate=8),

    ResearchDependency(TechInfo.IMPERIAL_AGE),
    Create(UnitInfo.KNIGHT,     time='04:00', rate=10),
    Research(TechInfo.CAVALIER, time='05:00'),
    Create(UnitInfo.KNIGHT,     time='16:00', rate=12),
    Research(TechInfo.PALADIN,  time='18:00'),
    # @formatter:on
]

camel_rider_line: list[Event] = [
    # @formatter:off
    ResearchDependency(TechInfo.CASTLE_AGE),
    Create(UnitInfo.CAMEL_RIDER,         time='00:00', rate=2),
    Create(UnitInfo.CAMEL_RIDER,         time='09:00', rate=4),
    Create(UnitInfo.CAMEL_RIDER,         time='14:00', rate=6),

    ResearchDependency(TechInfo.IMPERIAL_AGE),
    Research(TechInfo.HEAVY_CAMEL_RIDER, time='08:00'),
    Create(UnitInfo.CAMEL_RIDER,         time='09:00', rate=10),
    # @formatter:on
]

steppe_lancer_line: list[Event] = [
    # @formatter:off
    ResearchDependency(TechInfo.CASTLE_AGE),
    Create(UnitInfo.STEPPE_LANCER,         time='00:00', rate=1),
    Create(UnitInfo.STEPPE_LANCER,         time='08:00', rate=3),
    Create(UnitInfo.STEPPE_LANCER,         time='15:00', rate=5),
    Create(UnitInfo.STEPPE_LANCER,         time='20:00', rate=6),

    ResearchDependency(TechInfo.IMPERIAL_AGE),
    Research(TechInfo.ELITE_STEPPE_LANCER, time='12:00'),
    Create(UnitInfo.STEPPE_LANCER,         time='16:00', rate=8),
    # @formatter:on
]

battle_elephant_line: list[Event] = [
    # @formatter:off
    ResearchDependency(TechInfo.CASTLE_AGE),
    Create(UnitInfo.BATTLE_ELEPHANT, time='02:30', rate=1),
    Create(UnitInfo.BATTLE_ELEPHANT, time='05:00', rate=3),
    Create(UnitInfo.BATTLE_ELEPHANT, time='15:00', rate=8),

    ResearchDependency(TechInfo.IMPERIAL_AGE),
    Research(TechInfo.ELITE_BATTLE_ELEPHANT, time='10:00'),
    # @formatter:on
]
