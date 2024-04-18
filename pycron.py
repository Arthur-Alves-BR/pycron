import os
import time
import logging
import pendulum

from kernel.pycron_conf import read_config_file, get_schedule_and_command
from kernel.date_and_time import is_it_time_to_run, calc_seconds_until_next_run


def main() -> None:
    logging.basicConfig(
        filename='pycron.log',
        level=logging.WARNING,
        datefmt='%m/%d/%Y %I:%M:%S %p',
        format='%(asctime)s - %(levelname)s: %(message)s',
    )

    while True:
        reference_datetime = pendulum.now()

        for item in read_config_file():
            try:
                scheduling_parts, command = get_schedule_and_command(item)
                if is_it_time_to_run(reference_datetime, scheduling_parts):
                    _output = os.popen(command).read()
            except Exception as exc:
                logging.error(exc)

        time.sleep(calc_seconds_until_next_run(reference_datetime))


if __name__ == '__main__':
    main()
