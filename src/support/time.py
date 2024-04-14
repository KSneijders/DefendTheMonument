from __future__ import annotations


class Time:
    def __init__(self, hours: int, minutes: int, secs: int):
        self.hours = hours
        self.mins = minutes
        self.secs = secs

    @classmethod
    def from_time(cls, time: str):
        segments: list[str] = time.split(':')

        match len(segments):
            case 1:
                nmbrs = 0, 0, segments[0]
            case 2:
                nmbrs = 0, segments[0], segments[1]
            case 3:
                nmbrs = segments
            case _:
                raise ValueError('Invalid time format')

        hours, minutes, secs = nmbrs
        return cls(hours=int(hours), minutes=int(minutes), secs=int(secs))

    @staticmethod
    def to_seconds(time: str) -> int:
        time = Time.from_time(time)
        return (time.hours * 60 * 60) + (time.mins * 60) + time.secs

    @staticmethod
    def from_seconds(secs: int) -> Time:
        hours = secs // 3600
        minutes = (secs % 3600) // 60
        seconds = (secs % 3600) % 60
        return Time(hours, minutes, seconds)

    def __str__(self):
        return f"{self.hours:02d}:{self.mins:02d}:{self.secs:02d}"
