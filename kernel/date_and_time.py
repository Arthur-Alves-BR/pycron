import typing
import pendulum


PART_TYPES = ('MINUTE', 'HOUR', 'DAY', 'MONTH', 'YEAR')


def calc_seconds_until_next_run(reference: pendulum.DateTime) -> int:
    return 60 - reference.second


def is_it_time_to_run(reference: pendulum.DateTime, scheduling_parts: typing.List[str]) -> bool:
    for index, part in enumerate(scheduling_parts):
        part_type = PART_TYPES[index].lower()
        if part == '*':
            continue
        if part.isnumeric() and int(part) == getattr(reference, part_type):
            continue
        return False
    return True
