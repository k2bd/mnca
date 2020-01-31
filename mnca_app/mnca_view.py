import numpy as np
from traits.api import Instance, Button
from traitsui.api import (
    HSplit,
    Item,
    ModelView,
    UItem,
    VGroup,
    View,
    VSplit,
)

from mnca_app.rule import Rule, LIFE, DEATH
from mnca_app.mnca_model import MncaModel
from mnca_app.mnca_board_editor import BoolArrayEditor


class MncaView(ModelView):

    model = Instance(MncaModel, allow_none=False)

    randomize_rules = Button("Randomize Rules")

    def _randomize_rules_fired(self):
        self.model.randomize_rules()

    reset_board = Button("Reset Board")

    def _reset_board_fired(self):
        self.model.reset_board()

    def default_traits_view(self):
        view = View(
            HSplit(
                UItem(
                    "model.board",
                    editor=BoolArrayEditor(
                        scale=True,
                        allow_upscaling=False,
                        allow_clipping=False,
                        preserve_aspect_ratio=True,
                    ),
                    resizable=True,
                    springy=True,
                ),
                VSplit(
                    VGroup(
                        Item("model.paused", label="Pause"),
                        Item("model.board_size"),
                    ),
                    VGroup(
                        Item("model.reset_life_pct", label="Reset Life %"),
                        Item("reset_board"),
                    )
                ),
                VGroup(
                    Item("model.rules"),
                    Item("randomize_rules"),
                ),
                springy=True,
            ),
            resizable=True,
        )
        return view


if __name__ == "__main__":
    model = MncaModel(
        board_size=(400, 400),
    )

    import os
    # Add masks
    #mask_files = ["mask_a", "mask_b", "mask_c", "mask_d"]
    model.masks = {}
    for m_file in os.listdir("mnca_app/data/masks"):
        with open(os.path.join("mnca_app", "data", "masks", m_file), "r") as f:
            mask = [[int(n) for n in line.split()] for line in f.readlines()]
            model.masks[m_file] = np.array(mask)

    # Add rules
    model.rules = [
        Rule(mask="8_neighbor.txt", limits=(3, 7), result=DEATH),
        Rule(mask="8_neighbor.txt", limits=(2, 5), result=DEATH),
        Rule(mask="1w1l.txt", limits=(1, 1), result=DEATH),
        Rule(mask="1w1l.txt", limits=(1, 4), result=LIFE),
        Rule(mask="9_neighbor.txt", limits=(6, 9), result=LIFE),
        Rule(mask="1w2l.txt", limits=(1, 5), result=LIFE),
        Rule(mask="9_neighbor.txt", limits=(0, 7), result=DEATH),
        Rule(mask="9_neighbor.txt", limits=(1, 4), result=LIFE),
        Rule(mask="8_neighbor.txt", limits=(6, 8), result=DEATH),
    ]

    view = MncaView(model=model)
    view.edit_traits(kind="livemodal")
