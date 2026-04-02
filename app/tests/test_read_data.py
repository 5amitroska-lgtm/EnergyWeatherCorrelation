import pytest
def test_example():
    assert 1==1

def test_example2():
    with pytest.raises(ZeroDivisionError):
        1/0
