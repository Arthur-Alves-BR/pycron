import pytest
import typing
import pendulum

from kernel.date_and_time import is_it_time_to_run
from kernel.pycron_conf import get_schedule_and_command


@pytest.mark.parametrize('test_input,expected_output', [
    (
        r'* * * * * python "C:\path\to folder\script.py"',
        (['*', '*', '*', '*', '*'], r'python "C:\path\to folder\script.py"')
    ),
    (
        '0 0 1 5 * python /path/to_folder/script.py',
        (['0', '0', '1', '5', '*'], 'python /path/to_folder/script.py')
    ),
    (
        '0    0    1    5    *    python    /path/to_folder/script.py',
        (['0', '0', '1', '5', '*'], 'python /path/to_folder/script.py')
    )
])
def test_get_schedule_and_command(test_input: str, expected_output: tuple) -> None:
    assert get_schedule_and_command(test_input) == expected_output


@pytest.mark.parametrize('scheduling_parts,expected_output', [
    (['*', '*', '*', '*', '*'], True),
    (['0', '*', '*', '*', '*'], True),
    (['0', '0', '*', '*', '*'], True),
    (['0', '0', '1', '*', '*'], True),
    (['0', '1', '*', '*', '*'], False),
    (['0', '0', '0', '*', '*'], False),
    (['1', '*', '*', '*', '*'], False),
    (['0', '0', '1', '1', '2024'], True)
])
def test_is_it_time_to_run(scheduling_parts: typing.List[str], expected_output: bool) -> None:
    reference = pendulum.DateTime(year=2024, month=1, day=1, hour=0, minute=0, second=0)
    pendulum.travel_to(reference, freeze=True)
    assert is_it_time_to_run(reference, scheduling_parts) == expected_output
