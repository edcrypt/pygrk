import pytest
from scales import AbstractBaseScale, MajorScale, GraphMajorScale


@pytest.mark.parametrize(
        'scale_class',
        (MajorScale, GraphMajorScale),
)
def test_major_mode(scale_class: AbstractBaseScale):
    assert str(scale_class.generate_scale("C")) == 'C D E F G A B C'

@pytest.mark.parametrize(
        'scale_class',
        (MajorScale, GraphMajorScale),
)
def test_modes(scale_class):
    assert str(scale_class.generate_scale("F", mode=scale_class.Modes.Lydian)) == 'F G A B C D E F'
    assert str(scale_class.generate_scale("C", mode=scale_class.Modes.Lydian)) == 'C D E F# G A B C'
