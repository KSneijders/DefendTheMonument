from AoE2ScenarioParser.datasets.techs import TechInfo
from AoE2ScenarioParser.datasets.units import UnitInfo

from src.generate.events.events import Research, ResearchDependency, Create, Event

barracks_techs: list[Event] = [
    # @formatter:off
    ResearchDependency(TechInfo.FEUDAL_AGE),

    Research(TechInfo.SUPPLIES,         time='05:00'),  # SUPPLIESS!

    ResearchDependency(TechInfo.CASTLE_AGE),

    Research(TechInfo.SQUIRES,          time='02:30'),
    Research(TechInfo.GAMBESONS,        time='05:00'),
    Research(TechInfo.ARSON,            time='10:00'),
    # @formatter:on
]

militia_line: list[Event] = [
    # @formatter:off
    Create(UnitInfo.MILITIA,                time='00:08', rate=3),
    Create(UnitInfo.MILITIA,                time='01:00', rate=4),
    Create(UnitInfo.MILITIA,                time='02:00', rate=5),
    Create(UnitInfo.MILITIA,                time='04:00', rate=6),
    Create(UnitInfo.MILITIA,                time='06:00', rate=8),
    Create(UnitInfo.MILITIA,                time='08:00', rate=9),
    Create(UnitInfo.MILITIA,                time='09:00', rate=10),

    ResearchDependency(TechInfo.FEUDAL_AGE),
    Create(UnitInfo.MILITIA,                time='00:00', rate=12),
    Research(TechInfo.MAN_AT_ARMS,          time='01:00'),

    ResearchDependency(TechInfo.CASTLE_AGE),
    Research(TechInfo.LONG_SWORDSMAN,       time='02:00'),

    ResearchDependency(TechInfo.IMPERIAL_AGE),
    Research(TechInfo.TWO_HANDED_SWORDSMAN, time='02:00'),
    Research(TechInfo.CHAMPION,             time='10:00'),

    # IncrementalCreation(UnitInfo.MILITIA,   rate=1)
    # @formatter:on
]

spearman_line: list[Event] = [
    # @formatter:off
    ResearchDependency(TechInfo.FEUDAL_AGE),
    Create(UnitInfo.SPEARMAN,     time='00:00', rate=2),
    Create(UnitInfo.SPEARMAN,     time='03:00', rate=4),
    Create(UnitInfo.SPEARMAN,     time='08:00', rate=8),

    ResearchDependency(TechInfo.CASTLE_AGE),
    Research(TechInfo.PIKEMAN,    time='04:00'),
    Create(UnitInfo.SPEARMAN,     time='05:00', rate=10),

    ResearchDependency(TechInfo.IMPERIAL_AGE),
    Research(TechInfo.HALBERDIER, time='08:00'),
    # @formatter:on
]

eagle_line: list[Event] = [
    # @formatter:off
    ResearchDependency(TechInfo.FEUDAL_AGE),
    Create(UnitInfo.EAGLE_SCOUT,           time='00:00', rate=1),
    Create(UnitInfo.EAGLE_SCOUT,           time='02:00', rate=3),
    Create(UnitInfo.EAGLE_SCOUT,           time='05:00', rate=8),

    ResearchDependency(TechInfo.CASTLE_AGE),
    Research(TechInfo.EAGLE_WARRIOR,       time='01:30'),
    Create(UnitInfo.EAGLE_SCOUT,           time='04:00', rate=12),
    Create(UnitInfo.EAGLE_SCOUT,           time='09:00', rate=16),
    Create(UnitInfo.EAGLE_SCOUT,           time='14:00', rate=20),

    ResearchDependency(TechInfo.IMPERIAL_AGE),
    Create(UnitInfo.EAGLE_SCOUT,           time='02:00', rate=26),
    Create(UnitInfo.EAGLE_SCOUT,           time='05:00', rate=30),
    Research(TechInfo.ELITE_EAGLE_WARRIOR, time='07:00'),
    # @formatter:on
]

condottiero_line: list[Event] = [
    # @formatter:off
    ResearchDependency(TechInfo.IMPERIAL_AGE),
    Create(UnitInfo.CONDOTTIERO,           time='00:00', rate=6),
    Create(UnitInfo.CONDOTTIERO,           time='05:00', rate=10),
    Create(UnitInfo.CONDOTTIERO,           time='10:00', rate=15),
    Create(UnitInfo.CONDOTTIERO,           time='15:00', rate=20),
    # @formatter:on
]
