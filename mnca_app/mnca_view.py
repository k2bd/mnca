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
                        Item("model.rules"),
                        Item("randomize_rules"),
                    ),
                    VGroup(
                        Item("model.reset_life_pct", label="Reset Life %"),
                        Item("reset_board"),
                    )
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
    mask_files = ["mask_a", "mask_b", "mask_c", "mask_d"]
    model.masks = {}
    for m_file in mask_files:
        with open(os.path.join("mnca_app", "data", "masks", m_file+".txt"), "r") as f:
            mask = [[int(n) for n in line.split()] for line in f.readlines()]
            model.masks[m_file] = np.array(mask)

    # Add rules
    model.rules = [
        Rule(mask=mask_files[0], limits=(0, 17), result=DEATH),
        Rule(mask=mask_files[0], limits=(40, 42), result=LIFE),
        Rule(mask=mask_files[1], limits=(10, 13), result=LIFE),
        Rule(mask=mask_files[2], limits=(9, 21), result=DEATH),
        Rule(mask=mask_files[3], limits=(78, 89), result=DEATH),
        Rule(mask=mask_files[3], limits=(108, None), result=DEATH),
    ]

    view = MncaView(model=model)
    view.edit_traits(kind="livemodal")
