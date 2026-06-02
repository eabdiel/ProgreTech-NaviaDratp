from src.engine.coordinates import in_bounds


def test_coordinates_in_bounds():
    assert in_bounds(0, 0)
    assert in_bounds(6, 6)


def test_coordinates_out_of_bounds():
    assert not in_bounds(-1, 0)
    assert not in_bounds(0, 7)
