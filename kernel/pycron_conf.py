import typing


CONFIG_FILE = 'pycron_conf'


def read_config_file() -> typing.List[str]:
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as fp:
            return fp.readlines()
    except FileNotFoundError:
        return []


def get_schedule_and_command(pycron_item: str) -> typing.Tuple[typing.List[str], str]:
    splitted_item = pycron_item.split()
    schedule = splitted_item[:5]
    command = ' '.join(splitted_item[5:])
    return schedule, command


def is_comment(line: str) -> bool:
    return line.startswith('#')