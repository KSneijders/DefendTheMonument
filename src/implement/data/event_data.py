from AoE2ScenarioParser.datasets.buildings import BuildingInfo
from AoE2ScenarioParser.datasets.techs import TechInfo
from AoE2ScenarioParser.datasets.units import UnitInfo

from src.implement.builders.spawner_builder import SpawnerBuilder
from src.implement.events.events import Research, ResearchDependency, Create, Event
from src.implement.types.types import SectionType

ages: list[Event] = [
    # @formatter:off
    Research(TechInfo.FEUDAL_AGE,   time='10:00'),  # 10:00

    ResearchDependency(TechInfo.FEUDAL_AGE),
    Research(TechInfo.CASTLE_AGE,   time='12:00'),  # 22:00

    ResearchDependency(TechInfo.CASTLE_AGE),
    Research(TechInfo.IMPERIAL_AGE, time='18:00'),  # 40:00
    # @formatter:on
]

monk_line: list[Event] = [
    ResearchDependency(TechInfo.CASTLE_AGE),

    Create(UnitInfo.MONK, time='02:00', rate=3),
    Create(UnitInfo.MONK, time='05:00', rate=6),
    Create(UnitInfo.MONK, time='10:00', rate=9),
]

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

militia_line: list[Event] = [
    # @formatter:off
    Create(UnitInfo.MILITIA,                time='00:08', rate=3),
    Create(UnitInfo.MILITIA,                time='03:00', rate=5),
    Create(UnitInfo.MILITIA,                time='06:00', rate=7),

    ResearchDependency(TechInfo.FEUDAL_AGE),
    Research(TechInfo.MAN_AT_ARMS,          time='01:00'),
    Create(UnitInfo.MILITIA,                time='01:00', rate=9),

    ResearchDependency(TechInfo.CASTLE_AGE),
    Research(TechInfo.LONG_SWORDSMAN,       time='02:00'),

    ResearchDependency(TechInfo.IMPERIAL_AGE),
    Research(TechInfo.TWO_HANDED_SWORDSMAN, time='02:00'),
    Research(TechInfo.CHAMPION,             time='10:00'),

    # IncrementalCreation(UnitInfo.MILITIA,   rate=1)
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
    Create(UnitInfo.ARCHER,        time='03:00', rate=12),
    Create(UnitInfo.ARCHER,        time='05:00', rate=15),

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
    Research(TechInfo.IMPERIAL_SKIRMISHER, time='05:00'),
    # @formatter:on
]

scout_line: list[Event] = [
    # @formatter:off
    ResearchDependency(TechInfo.FEUDAL_AGE),
    Create(UnitInfo.SCOUT_CAVALRY,   time='02:00', rate=5),
    Create(UnitInfo.SCOUT_CAVALRY,   time='05:00', rate=8),

    ResearchDependency(TechInfo.CASTLE_AGE),
    Research(TechInfo.LIGHT_CAVALRY, time='02:30'),
    Create(UnitInfo.SCOUT_CAVALRY,   time='10:00', rate=12),

    ResearchDependency(TechInfo.IMPERIAL_AGE),
    Create(UnitInfo.SCOUT_CAVALRY,   time='04:00', rate=15),
    Research(TechInfo.HUSSAR,        time='08:00'),
    # @formatter:on
]

knight_line: list[Event] = [
    # @formatter:off
    ResearchDependency(TechInfo.CASTLE_AGE),
    Create(UnitInfo.KNIGHT,     time='00:00', rate=2),
    Create(UnitInfo.KNIGHT,     time='10:00', rate=5),
    Create(UnitInfo.KNIGHT,     time='20:00', rate=12),

    ResearchDependency(TechInfo.IMPERIAL_AGE),
    Research(TechInfo.CAVALIER, time='05:00'),
    Research(TechInfo.PALADIN,  time='18:00'),
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

blacksmith_techs: list[Event] = [
    # @formatter:off
    ResearchDependency(TechInfo.FEUDAL_AGE),
    Research(TechInfo.FLETCHING,            time='03:00'),
    Research(TechInfo.FORGING,              time='04:00'),
    Research(TechInfo.SCALE_MAIL_ARMOR,     time='05:00'),
    Research(TechInfo.PADDED_ARCHER_ARMOR,  time='06:30'),
    Research(TechInfo.SCALE_BARDING_ARMOR,  time='08:00'),

    ResearchDependency(TechInfo.CASTLE_AGE),
    Research(TechInfo.BODKIN_ARROW,         time='03:00'),
    Research(TechInfo.IRON_CASTING,         time='04:00'),
    Research(TechInfo.CHAIN_MAIL_ARMOR,     time='07:00'),
    Research(TechInfo.CHAIN_BARDING_ARMOR,  time='08:00'),
    Research(TechInfo.LEATHER_ARCHER_ARMOR, time='10:00'),

    ResearchDependency(TechInfo.IMPERIAL_AGE),
    Research(TechInfo.BRACER,               time='05:00'),
    Research(TechInfo.PLATE_BARDING_ARMOR,  time='07:00'),
    Research(TechInfo.BLAST_FURNACE,        time='09:00'),
    Research(TechInfo.PLATE_MAIL_ARMOR,     time='10:30'),
    Research(TechInfo.RING_ARCHER_ARMOR,    time='12:00'),
    # @formatter:on
]

university_techs: list[Event] = [
    # @formatter:off
    ResearchDependency(TechInfo.CASTLE_AGE),
    Research(TechInfo.BALLISTICS,      time='10:00'),
    Research(TechInfo.GUARD_TOWER,     time='08:00'),

    ResearchDependency(TechInfo.IMPERIAL_AGE),
    Research(TechInfo.MASONRY,         time='00:00'),
    Research(TechInfo.MURDER_HOLES,    time='00:30'),
    Research(TechInfo.CHEMISTRY,       time='04:00'),
    Research(TechInfo.ARROWSLITS,      time='09:00'),
    Research(TechInfo.KEEP,            time='10:00'),
    Research(TechInfo.SIEGE_ENGINEERS, time='12:00'),
    Research(TechInfo.ARCHITECTURE,    time='15:00'),
    # @formatter:on
]

ram_line: list[Event] = [
    # @formatter:off
    ResearchDependency(TechInfo.CASTLE_AGE),

    Create(UnitInfo.BATTERING_RAM, time='00:00', rate=1),
    Create(UnitInfo.BATTERING_RAM, time='03:00', rate=2),
    Create(UnitInfo.BATTERING_RAM, time='05:00', rate=3),
    Create(UnitInfo.BATTERING_RAM, time='10:00', rate=5),
    Create(UnitInfo.BATTERING_RAM, time='16:00', rate=10),

    ResearchDependency(TechInfo.IMPERIAL_AGE),
    Research(TechInfo.CAPPED_RAM,    time='02:00'),
    Research(TechInfo.SIEGE_RAM,     time='08:00'),
    # @formatter:on
]

armored_elephant_line: list[Event] = [
    # @formatter:off
    ResearchDependency(TechInfo.CASTLE_AGE),

    Create(UnitInfo.ARMORED_ELEPHANT, time='00:00', rate=1),
    Create(UnitInfo.ARMORED_ELEPHANT, time='03:00', rate=2),
    Create(UnitInfo.ARMORED_ELEPHANT, time='05:00', rate=3),
    Create(UnitInfo.ARMORED_ELEPHANT, time='10:00', rate=5),
    Create(UnitInfo.ARMORED_ELEPHANT, time='16:00', rate=10),

    ResearchDependency(TechInfo.IMPERIAL_AGE),
    Research(TechInfo.SIEGE_ELEPHANT,     time='05:00'),
    # @formatter:on
]

mangonel_line: list[Event] = [
    # @formatter:off
    ResearchDependency(TechInfo.CASTLE_AGE),

    Create(UnitInfo.MANGONEL,       time='00:00', rate=1),
    Create(UnitInfo.MANGONEL,       time='05:00', rate=3),
    Create(UnitInfo.MANGONEL,       time='10:00', rate=5),
    Create(UnitInfo.MANGONEL,       time='18:00', rate=8),

    ResearchDependency(TechInfo.IMPERIAL_AGE),
    Research(TechInfo.ONAGER,       time='08:00'),
    Research(TechInfo.SIEGE_ONAGER, time='20:00'),
    # @formatter:on
]

scorpion_line: list[Event] = [
    # @formatter:off
    ResearchDependency(TechInfo.CASTLE_AGE),

    Create(UnitInfo.SCORPION,           time='00:00', rate=2),
    Create(UnitInfo.SCORPION,           time='05:00', rate=5),
    Create(UnitInfo.SCORPION,           time='10:00', rate=8),

    ResearchDependency(TechInfo.IMPERIAL_AGE),
    Create(UnitInfo.SCORPION,           time='00:00', rate=10),
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

archery_range_techs: list[Event] = [
    # @formatter:off
    ResearchDependency(TechInfo.CASTLE_AGE),

    Research(TechInfo.THUMB_RING,       time='09:00'),

    ResearchDependency(TechInfo.IMPERIAL_AGE),

    Research(TechInfo.PARTHIAN_TACTICS, time='05:00'),
    # @formatter:on
]

sections: SectionType = {
    # @formatter:off
    BuildingInfo.TOWN_CENTER:    [ages],
    BuildingInfo.BLACKSMITH:     [blacksmith_techs],
    BuildingInfo.UNIVERSITY:     [university_techs],

    BuildingInfo.BARRACKS:       [barracks_techs, militia_line],
    BuildingInfo.ARCHERY_RANGE:  [archery_range_techs, archer_line, skirmisher_line],
    BuildingInfo.STABLE:         [scout_line, knight_line, battle_elephant_line],
    BuildingInfo.SIEGE_WORKSHOP: [bbc_line, ram_line, armored_elephant_line, scorpion_line, mangonel_line],
    BuildingInfo.MONASTERY:      [monk_line],
    BuildingInfo.CASTLE:         [petard_line, trebuchet_line],
    # @formatter:on
}

if __name__ == '__main__':
    spawner = SpawnerBuilder(sections=sections)
    spawner.print()
