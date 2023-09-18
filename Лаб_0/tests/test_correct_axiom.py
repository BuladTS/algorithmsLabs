from algorithms.lab_0 import create_axiom
import pytest


@pytest.mark.parametrize('prime_axiom, iterations, expectation', [
    ('0', 3, '221[21[1[0]0]1[0]0]21[1[0]0]1[0]0'),
    ('0', 2, '21[1[0]0]1[0]0'),
    ('0', 1, '1[0]0')
])
def test_correct_axiom(prime_axiom, iterations, expectation):
    assert create_axiom(prime_axiom, iterations) == expectation
