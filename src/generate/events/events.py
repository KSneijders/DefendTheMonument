from AoE2ScenarioParser.datasets.techs import TechInfo
from AoE2ScenarioParser.datasets.units import UnitInfo


class Event:
    def __init__(self):
        pass


class TimeBasedEvent(Event):
    def __init__(self, time: str):
        super().__init__()
        self.time: str = time

    def __str__(self):
        return f"TimeBasedEvent at {self.time}"


class Create(TimeBasedEvent):
    def __init__(self, unit: UnitInfo, rate: int, time: str):
        super().__init__(time)
        self.unit: UnitInfo = unit
        self.rate: int = rate

    def __str__(self):
        return f"Spawn {self.rate} {self.unit.name} per minute"


class Research(TimeBasedEvent):
    def __init__(self, tech: TechInfo, time: str):
        super().__init__(time)
        self.tech: TechInfo = tech

    def __str__(self):
        return f"Research {self.tech.name}"


class ResearchDependency(Event):
    def __init__(self, tech: TechInfo):
        super().__init__()
        self.tech = tech

    def __str__(self):
        return f"ResearchDependency {self.tech.name}"
