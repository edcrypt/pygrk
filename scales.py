import abc
from enum import IntEnum
from typing import Optional
import networkx as nx

# Interval sizes - Half and Whole Tones
class Step(IntEnum):
    HT = 1
    WT = 2


HT = Step.HT
WT = Step.WT

Note = str
Mode = IntEnum
ScaleFormula = tuple[Step, ...]

CHROMATIC_WITH_SHARPS = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


class BaseScaleBuilder(abc.ABC):
    """The strategy used to build scales"""

    @abc.abstractmethod
    def fill_scale(self):
        return NotImplemented


class SimpleScaleBuilder(BaseScaleBuilder):
    """Simple scale build strategy"""

    def fill_scale(self, root_note: Note, chromatic_notes: list[Note], scale_formula: ScaleFormula) -> list[Note]:
        scale_notes = []
        root_note_index = chromatic_notes.index(root_note)
        for step in scale_formula:
            root_note_index = (root_note_index + step) % len(chromatic_notes)
            scale_notes.append(chromatic_notes[root_note_index])
        return scale_notes


# https://yulleyi.medium.com/algorithmic-approaches-to-music-theory-4dec4f70d77c
class GraphScaleBuilder(BaseScaleBuilder):
    """Graph-based scale builder strategy"""

    scale_graph: nx.DiGraph

    def __init__(self):
        super().__init__()
        self.scale_graph = nx.DiGraph()

    def fill_scale(self, root_note: Note, chromatic_notes: list[Note], scale_formula: ScaleFormula) -> list[Note]:
        self.fill_graph(chromatic_notes, scale_formula)
        return list(self.scale_graph.successors(root_note))

    def fill_graph(self, chromatic_notes: list[Note], scale_formula: ScaleFormula):
        for note in chromatic_notes:
            self.scale_graph.add_node(note)

        for root_note in chromatic_notes:
            root_note_index = chromatic_notes.index(root_note)
            for step in scale_formula:
                root_note_index = (root_note_index + step) % len(chromatic_notes)
                scale_note = chromatic_notes[root_note_index]

                # Add an edge from the root note to the scale note
                self.scale_graph.add_edge(root_note, scale_note)


class AbstractBaseScale(abc.ABC):
    base_formula: ScaleFormula
    chromatic_notes: list[Note]
    mode: Mode
    default_mode: Mode

    chromatic_scale_size: int
    root_note: Note
    scale_notes: list[Note]

    Modes: type[Mode]

    _buider: Optional[BaseScaleBuilder] = None

    def __init__(self, root_note: Note):
        self.root_note = root_note
        self.chromatic_scale_size = len(self.chromatic_notes)

    def __str__(self):
        return f'{self.root_note} {" ".join(self.scale_notes)}'

    @classmethod
    def generate_scale(cls, root_note: Note = 'C', mode: Optional[Mode] = None, builder: Optional[BaseScaleBuilder] = None):
        obj = cls(root_note)
        obj.mode = cls.default_mode if mode is None else mode
        builder = SimpleScaleBuilder() if builder is None else builder
        obj.fill_scale(builder=builder)
        return obj

    def mode_formula(self) -> ScaleFormula:
        """Rotate the scale formula according to the mode index"""
        if self.mode is self.default_mode:
            return self.base_formula
        return self.base_formula[self.mode:] + self.base_formula[:self.mode]

    def fill_scale(self, builder: BaseScaleBuilder):
        self._builder = builder
        self.scale_notes = builder.fill_scale(self.root_note, self.chromatic_notes, self.mode_formula())


class MajorScale(AbstractBaseScale):
    base_formula = (WT, WT, HT, WT, WT, WT, HT)
    chromatic_notes = CHROMATIC_WITH_SHARPS

    class Modes(IntEnum):
        Ionian = 0
        Dorian = 1
        Phrygian = 2
        Lydian = 3
        Mixolydian = 4
        Aeolian = 5
        Locrian = 6

    default_mode = Modes.Ionian
