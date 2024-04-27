from AoE2ScenarioParser.datasets.techs import TechInfo
from AoE2ScenarioParser.datasets.units import UnitInfo

from src.implement.events.events import Create, Research, ResearchDependency, Event

ram_line: list[Event] = [
    # @formatter:off
    ResearchDependency(TechInfo.CASTLE_AGE),

    Create(UnitInfo.BATTERING_RAM, time='00:00', rate=1),
    Create(UnitInfo.BATTERING_RAM, time='03:00', rate=2),
    Create(UnitInfo.BATTERING_RAM, time='07:00', rate=3),
    Create(UnitInfo.BATTERING_RAM, time='10:00', rate=5),
    Create(UnitInfo.BATTERING_RAM, time='16:00', rate=10),

    ResearchDependency(TechInfo.IMPERIAL_AGE),
    Research(TechInfo.CAPPED_RAM,    time='02:00'),
    Research(TechInfo.SIEGE_RAM,     time='14:00'),
    # @formatter:on
]

armored_elephant_line: list[Event] = [
    # @formatter:off
    ResearchDependency(TechInfo.CASTLE_AGE),

    Create(UnitInfo.ARMORED_ELEPHANT, time='00:00', rate=1),
    Create(UnitInfo.ARMORED_ELEPHANT, time='03:00', rate=2),
    Create(UnitInfo.ARMORED_ELEPHANT, time='07:00', rate=3),
    Create(UnitInfo.ARMORED_ELEPHANT, time='10:00', rate=5),
    Create(UnitInfo.ARMORED_ELEPHANT, time='16:00', rate=10),

    ResearchDependency(TechInfo.IMPERIAL_AGE),
    Research(TechInfo.SIEGE_ELEPHANT,     time='05:00'),
    # @formatter:on
]

mangonel_line: list[Event] = [
    # @formatter:off
    ResearchDependency(TechInfo.CASTLE_AGE),

    Create(UnitInfo.MANGONEL,       time='03:00', rate=1),
    Create(UnitInfo.MANGONEL,       time='05:00', rate=2),
    Create(UnitInfo.MANGONEL,       time='10:00', rate=3),
    Create(UnitInfo.MANGONEL,       time='18:00', rate=5),

    ResearchDependency(TechInfo.IMPERIAL_AGE),
    Research(TechInfo.ONAGER,       time='08:00'),
    Create(UnitInfo.MANGONEL,       time='12:00', rate=8),
    Research(TechInfo.SIEGE_ONAGER, time='20:00'),
    # @formatter:on
]

scorpion_line: list[Event] = [
    # @formatter:off
    ResearchDependency(TechInfo.CASTLE_AGE),

    Create(UnitInfo.SCORPION,           time='03:00', rate=2),
    Create(UnitInfo.SCORPION,           time='06:00', rate=4),
    Create(UnitInfo.SCORPION,           time='10:00', rate=8),
    Create(UnitInfo.SCORPION,           time='15:00', rate=12),

    ResearchDependency(TechInfo.IMPERIAL_AGE),
    Create(UnitInfo.SCORPION,           time='00:00', rate=15),
    Research(TechInfo.HEAVY_SCORPION,   time='10:00'),
    # @formatter:on
]

bbc_line: list[Event] = [
    # @formatter:off
    ResearchDependency(TechInfo.CHEMISTRY),
    Create(UnitInfo.BOMBARD_CANNON, time='00:00', rate=1),
    Create(UnitInfo.BOMBARD_CANNON, time='05:00', rate=3),
    Create(UnitInfo.BOMBARD_CANNON, time='10:00', rate=6),

    Research(TechInfo.HOUFNICE,     time='16:00'),

    Create(UnitInfo.BOMBARD_CANNON, time='15:00', rate=10),
    # @formatter:on
]