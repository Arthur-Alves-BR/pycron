import os
import time
import logging
import pendulum

from kernel.date_and_time import is_it_time_to_run, calc_seconds_until_next_run
from kernel.pycron_conf import read_config_file, get_schedule_and_command, is_comment


def handle_line(line: str, reference: pendulum.DateTime) -> None:
    try:
        scheduling_parts, command = get_schedule_and_command(line)
        if is_it_time_to_run(reference, scheduling_parts):
            _output = os.popen(command).read()
    except Exception as exc:
        logging.error(exc)


def main() -> None:
    logging.basicConfig(
        filename='pycron.log',
        level=logging.WARNING,
        datefmt='%m/%d/%Y %I:%M:%S %p',
        format='%(asctime)s - %(levelname)s: %(message)s',
    )
    while True:
        reference_instant = pendulum.now()
        for line in read_config_file():
            if is_comment(line):
                print(line)
                continue
            handle_line(line, reference_instant)
        time.sleep(calc_seconds_until_next_run(reference_instant))


if __name__ == '__main__':
    main()
