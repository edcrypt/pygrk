import pytest
from scales import MajorScale, BaseScaleBuilder, SimpleScaleBuilder, GraphScaleBuilder


@pytest.mark.parametrize(
        'scale_builder',
        (SimpleScaleBuilder(), GraphScaleBuilder()),
)
def test_major_mode(scale_builder: BaseScaleBuilder):
    scale = MajorScale.generate_scale("C", builder=scale_builder)
    assert str(scale) == 'C D E F G A B C'

@pytest.mark.parametrize(
        'scale_builder',
        (SimpleScaleBuilder(), GraphScaleBuilder()),
)
def test_modes(scale_builder: BaseScaleBuilder):
    assert str(MajorScale.generate_scale("F", mode=MajorScale.Modes.Lydian, builder=scale_builder)) == 'F G A B C D E F'
    assert str(MajorScale.generate_scale("C", mode=MajorScale.Modes.Lydian, builder=scale_builder)) == 'C D E F# G A B C'
