import pytest

import math

import hypothesis.strategies as st

from hypothesis import given, seed

from utils import my_power, my_sqrt, my_round


# @given(st.floats(), st.integers())
# def test_my_power_hypothesis(number, my_power_number):
#     my_result = my_power(number, my_power_number)


# @given(st.floats(min_value=0))
# def test_my_sqrt_hypothesis(number):
#     print("number = ", number)
#     my_result = math.sqrt(number)
#     my_result = my_sqrt(number)


# @given(st.floats(), st.integers(min_value=0, max_value=20))
# def test_my_round_hypothesis(number, precision):
#     my_result = my_round(number, precision)


# def test_my_power():
#     assert my_power(number=0, power=1500) == 0
#     assert my_power(number=0, power=-1500) == 0
#     assert my_power(number=0, power=0) == 1
#     assert my_power(number=500, power=0) == 1
#     assert my_power(number=-500, power=0) == 1
#     assert my_power(number=-4.54221, power=0) == 1
#     assert my_power(number=4.54221, power=0) == 1
#     assert my_power(number=5, power=5) == 3125
#     assert my_power(number=5, power=1000000000) == float("infinity")
#     assert my_power(number=5, power=-1000000000) == 0
#     with pytest.raises(ValueError) as e:
#         ret = my_power(number=5, power=0.0000000000000000001) == 0
#     assert str(e.value) == "irrational numbers are not accepted as exponent."
#     assert str(e.value) == "irrational numbers are not accepted as exponent."
#     assert my_power(number=0.0000000000000000000000000000001, power=2) == 1.0000000000000003e-62
#     assert my_power(number=999999999999999999999999999999999999999, power=2) == float("infinity")
#     assert my_power(number=3, power=-3) == 0.037037037037037035


def test_my_sqrt():
    assert my_sqrt(number=4) == 2
    assert my_sqrt(number=16) == 4
    assert my_sqrt(number=16.545) == 4.067554547882548
    assert my_sqrt(number=0.5454575) == 0.738550946110016
    assert my_sqrt(number=1758) == 41.92851058647326
    assert my_sqrt(number=99999999999999) == 9999999.99999995
    assert my_sqrt(number=99999999999999999) == 316227766.01683795


def test_my_round():
    # Test round up
    assert my_round(10.025, 2) == 10.03

    # Test multiple round up
    assert my_round(19.9951, 2) == 20.00

    assert my_round(10, 2) == 10

    with pytest.raises(ValueError) as e:
        my_round(10, 200000000) == 10
    assert str(e.value) == "Precision should be between 0 and 20"

    assert my_round(10, 20) == 10
    assert my_round(10, 0) == 10

    assert my_round(10.01234567891011121314555555555, 20) == 10.01234567891011121314555555555
    assert my_round(10.01234567891011121314555555555, 18) == 10.01234567891011121314555555555

    assert my_round(10.025, 10) == 10.025
    assert my_round(10.025454555557885454242, 10) == 10.0254545556

    assert my_round(10.025, 20) == 10.025
    assert my_round(10.025454555557885454242, 20) == 10.025454555557885454242
    assert my_round(10.0254545555578854542424444447585876545645, 20) == 10.025454555557885454242

    assert my_round(0.00000000000000000000000009, 20) == 0
    assert my_round(1.11111115e2, 1) == 111.1

    # Big round
    assert my_round(99999999999999999999999999999999999999, 20) == 1e38

    # small round
    assert my_round(1e-100000, 20) == 0

    pass
