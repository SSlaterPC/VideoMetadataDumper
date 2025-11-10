# Imports
import pytest


# tests
@pytest.mark.parametrize('input', 'expected', [
    ('', ''),
])
def test_test(input, expected):
    assert 1 == 1
    assert not 1 == 1

def test_test2():
    assert 1 == 1
    assert not 1 == 1
