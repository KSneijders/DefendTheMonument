from AoE2ScenarioParser.datasets.techs import TechInfo
from AoE2ScenarioParser.datasets.units import UnitInfo

from src.implement.events.events import Create, ResearchDependency, Research, Event

monastery_techs: list[Event] = [
    # @formatter:off
    ResearchDependency(TechInfo.CASTLE_AGE),
    Research(TechInfo.HERBAL_MEDICINE,         time='00:00'),
    Research(TechInfo.FERVOR,                  time='01:30'),
    Research(TechInfo.SANCTITY,                time='03:00'),
    Research(TechInfo.DEVOTION,                time='07:00'),
    Research(TechInfo.ATONEMENT,               time='09:00'),
    Research(TechInfo.REDEMPTION,              time='12:00'),

    ResearchDependency(TechInfo.IMPERIAL_AGE),
    Research(TechInfo.THEOCRACY,               time='00:00'),
    Research(TechInfo.ILLUMINATION,            time='03:00'),
    Research(TechInfo.BLOCK_PRINTING,          time='10:00'),
    Research(TechInfo.FAITH,                   time='12:00'),

    Research(TechInfo.HERESY,                  time='16:00'),
    # @formatter:on
]

monk_line: list[Event] = [
    ResearchDependency(TechInfo.CASTLE_AGE),

    Create(UnitInfo.MONK, time='02:00', rate=3),
    Create(UnitInfo.MONK, time='06:00', rate=6),
    Create(UnitInfo.MONK, time='10:00', rate=9),
]
