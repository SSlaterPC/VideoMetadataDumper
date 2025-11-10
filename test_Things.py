# Imports
import pytest


# tests
@pytest.mark.parametrize('input, expected', [
    ('', ''),
    (1, 2),
])
def test_test(input, expected):
    print(input, expected)
    assert True

