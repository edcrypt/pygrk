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


class AbstractBaseScale(abc.ABC):
    base_formula: ScaleFormula
    chromatic_notes: list[Note]
    mode: Mode
    default_mode: Mode

    chromatic_scale_size: int
    root_note: Note
    scale_notes: list[Note]

    Modes: type[Mode]

    def __init__(self, root_note: Note):
        self.root_note = root_note
        self.chromatic_scale_size = len(self.chromatic_notes)

    def __str__(self):
        return f'{self.root_note} {" ".join(self.scale_notes)}'

    @classmethod
    def generate_scale(cls, root_note: Note = 'C', mode: Optional[Mode] = None):
        obj = cls(root_note)
        obj.mode = cls.default_mode if mode is None else mode
        obj.fill_scale()
        return obj

    def mode_formula(self) -> ScaleFormula:
        """Rotate the scale formula according to the mode index"""
        if self.mode is self.default_mode:
            return self.base_formula
        return self.base_formula[self.mode:] + self.base_formula[:self.mode]

    @abc.abstractmethod
    def fill_scale(self):
        return NotImplemented


class SimpleBaseScale(AbstractBaseScale):
    
    def fill_scale(self):
        scale_notes = []
        root_note_index = self.chromatic_notes.index(self.root_note)
        for step in self.mode_formula():
            root_note_index = (root_note_index + step) % self.chromatic_scale_size
            scale_notes.append(self.chromatic_notes[root_note_index])
        self.scale_notes = scale_notes


# https://yulleyi.medium.com/algorithmic-approaches-to-music-theory-4dec4f70d77c
class GraphBaseScale(AbstractBaseScale):
    scale_graph: nx.DiGraph

    def __init__(self, root_note: Note):
        super().__init__(root_note=root_note)
        self.scale_graph = nx.DiGraph()

    def fill_scale(self):
        self.fill_graph()
        self.scale_notes = list(self.scale_graph.successors(self.root_note))

    def fill_graph(self):
        for note in self.chromatic_notes:
            self.scale_graph.add_node(note)

        for root_note in self.chromatic_notes:
            root_note_index = self.chromatic_notes.index(root_note)
            for step in self.mode_formula():
                root_note_index = (root_note_index + step) % 12
                scale_note = self.chromatic_notes[root_note_index]

                # Add an edge from the root note to the scale note
                self.scale_graph.add_edge(root_note, scale_note)


class MajorScale(SimpleBaseScale):
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


class GraphMajorScale(GraphBaseScale):
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
