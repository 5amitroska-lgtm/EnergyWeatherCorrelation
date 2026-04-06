import pytest
def test_example():
    assert 1==1

def test_example2():
    with pytest.raises(ZeroDivisionError):
        1/0

@pytest.fixture
def f():
    return 1/0

@pytest.mark.parametrize(
    "number,expected_balance",
    [
        (1, 1),
        (1,2)
    ]
)
def test_example3(number,expected_balance):
    assert number == expected_balance