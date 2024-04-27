from AoE2ScenarioParser.datasets.techs import TechInfo
from AoE2ScenarioParser.datasets.units import UnitInfo

from src.implement.events.events import Create, ResearchDependency, Event, Research

castle_techs: list[Event] = [
    # ResearchDependency(TechInfo.CASTLE_AGE),
    # Todo: CASTLE_AGE Unique Tech

    ResearchDependency(TechInfo.IMPERIAL_AGE),
    # Todo: IMPERIAL_AGE Unique Tech

    Research(TechInfo.CONSCRIPTION, time='05:00'),
    Research(TechInfo.HOARDINGS,    time='12:00'),

    # IncrementalCreation(UnitInfo.PETARD, rate=1)
]

# Todo: unique_unit_line: list[Event] = []

petard_line: list[Event] = [
    ResearchDependency(TechInfo.CASTLE_AGE),

    Create(UnitInfo.PETARD, time='00:00', rate=2),
    Create(UnitInfo.PETARD, time='06:00', rate=4),
    Create(UnitInfo.PETARD, time='10:00', rate=6),
    Create(UnitInfo.PETARD, time='16:00', rate=10),
    Create(UnitInfo.PETARD, time='20:00', rate=12),

    ResearchDependency(TechInfo.IMPERIAL_AGE),

    Create(UnitInfo.PETARD, time='00:00', rate=16),

    # IncrementalCreation(UnitInfo.PETARD, rate=1)
]

trebuchet_line: list[Event] = [
    # @formatter:off
    ResearchDependency(TechInfo.IMPERIAL_AGE),
    Create(UnitInfo.TREBUCHET, time='00:00', rate=1),
    Create(UnitInfo.TREBUCHET, time='05:00', rate=3),
    Create(UnitInfo.TREBUCHET, time='10:00', rate=5),
    Create(UnitInfo.TREBUCHET, time='15:00', rate=8),
    Create(UnitInfo.TREBUCHET, time='20:00', rate=10),
    # @formatter:on
]