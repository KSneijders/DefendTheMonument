from AoE2ScenarioParser.datasets.buildings import BuildingInfo
from AoE2ScenarioParser.datasets.techs import TechInfo

from src.generate.builders.spawner_builder import SpawnerBuilder
from src.generate.data.events.archery_range import archery_range_techs, skirmisher_line, archer_line, \
    cavalry_archer_line, hand_cannoneer_line, elephant_archer_line, genitour_line, slinger_line
from src.generate.data.events.barracks import barracks_techs, militia_line, spearman_line, eagle_line, condottiero_line
from src.generate.data.events.castle import trebuchet_line, petard_line, castle_techs
from src.generate.data.events.monastery import monastery_techs, monk_line, missionary_line
from src.generate.data.events.siege_workshop import mangonel_line, scorpion_line, armored_elephant_line, ram_line, \
    bbc_line
from src.generate.data.events.stable import battle_elephant_line, knight_line, scout_line, stable_techs, \
    camel_rider_line, steppe_lancer_line
from src.generate.events.events import Research, ResearchDependency, Create, Event
from src.generate.types.types import SectionType

ages: list[Event] = [
    # @formatter:off
    Research(TechInfo.FEUDAL_AGE,   time='10:00'),  # 10:00

    ResearchDependency(TechInfo.FEUDAL_AGE),
    Research(TechInfo.CASTLE_AGE,   time='12:00'),  # 22:00

    ResearchDependency(TechInfo.CASTLE_AGE),
    Research(TechInfo.IMPERIAL_AGE, time='18:00'),  # 40:00
    # @formatter:on
]

blacksmith_techs: list[Event] = [
    # @formatter:off
    ResearchDependency(TechInfo.FEUDAL_AGE),
    Research(TechInfo.FLETCHING,            time='03:00'),
    Research(TechInfo.FORGING,              time='04:00'),
    Research(TechInfo.SCALE_MAIL_ARMOR,     time='05:00'),
    Research(TechInfo.PADDED_ARCHER_ARMOR,  time='08:00'),
    Research(TechInfo.SCALE_BARDING_ARMOR,  time='11:00'),

    ResearchDependency(TechInfo.CASTLE_AGE),
    Research(TechInfo.BODKIN_ARROW,         time='02:00'),
    Research(TechInfo.IRON_CASTING,         time='05:00'),
    Research(TechInfo.CHAIN_MAIL_ARMOR,     time='09:00'),
    Research(TechInfo.CHAIN_BARDING_ARMOR,  time='13:00'),
    Research(TechInfo.LEATHER_ARCHER_ARMOR, time='17:00'),

    ResearchDependency(TechInfo.IMPERIAL_AGE),
    Research(TechInfo.BRACER,               time='04:00'),
    Research(TechInfo.PLATE_BARDING_ARMOR,  time='07:00'),
    Research(TechInfo.BLAST_FURNACE,        time='09:00'),
    Research(TechInfo.PLATE_MAIL_ARMOR,     time='12:00'),
    Research(TechInfo.RING_ARCHER_ARMOR,    time='15:00'),
    # @formatter:on
]

university_techs: list[Event] = [
    # @formatter:off
    ResearchDependency(TechInfo.CASTLE_AGE),
    Research(TechInfo.BALLISTICS,      time='10:00'),
    Research(TechInfo.GUARD_TOWER,     time='08:00'),

    ResearchDependency(TechInfo.IMPERIAL_AGE),
    Research(TechInfo.MASONRY,         time='00:00'),
    Research(TechInfo.MURDER_HOLES,    time='01:00'),
    Research(TechInfo.CHEMISTRY,       time='04:00'),
    Research(TechInfo.ARROWSLITS,      time='09:00'),
    Research(TechInfo.KEEP,            time='10:00'),
    Research(TechInfo.SIEGE_ENGINEERS, time='12:00'),
    Research(TechInfo.ARCHITECTURE,    time='15:00'),
    # @formatter:on
]

sections: SectionType = {
    # @formatter:off
    BuildingInfo.TOWN_CENTER:    [ages],
    BuildingInfo.BLACKSMITH:     [blacksmith_techs],
    BuildingInfo.UNIVERSITY:     [university_techs],

    BuildingInfo.BARRACKS:       [barracks_techs, militia_line, spearman_line, eagle_line, condottiero_line],
    BuildingInfo.ARCHERY_RANGE:  [archery_range_techs, archer_line, skirmisher_line, cavalry_archer_line, elephant_archer_line, hand_cannoneer_line, genitour_line, slinger_line],
    BuildingInfo.STABLE:         [stable_techs, scout_line, knight_line, camel_rider_line, steppe_lancer_line, battle_elephant_line],
    BuildingInfo.SIEGE_WORKSHOP: [ram_line, armored_elephant_line, mangonel_line, scorpion_line, bbc_line],
    BuildingInfo.MONASTERY:      [monastery_techs, monk_line, missionary_line],
    BuildingInfo.CASTLE:         [castle_techs, petard_line, trebuchet_line],
    # @formatter:on
}

if __name__ == '__main__':
    spawner = SpawnerBuilder(sections=sections)
    spawner.print()
