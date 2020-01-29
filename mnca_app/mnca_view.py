import numpy as np
from traits.api import Instance, Button
from traitsui.api import (
    ModelView,
    HSplit,
    VGroup,
    View,
    Item,
    UItem,
)

from mnca_app.rule import Rule, LIFE, DEATH
from mnca_app.mnca_model import MncaModel, RANDOM
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
                        allow_clipping=True,
                        #update_ms=600,
                    ),
                ),
                VGroup(
                    Item("model.paused", label="Pause"),
                    Item("model.board_size"),
                    Item("randomize_rules"),
                    Item("reset_board"),
                ),
            ),
            resizable=True,
        )
        return view


if __name__ == "__main__":
    model = MncaModel(
        board_size=(500, 500),
        reset_style=RANDOM,
    )

    import os
    # Add masks
    mask_files = ["mask_a.txt", "mask_b.txt", "mask_c.txt", "mask_d.txt",]
    model.masks = []
    for m_file in mask_files:
        with open(os.path.join("mnca_app", "data", "masks", m_file), "r") as f:
            mask = [[int(n) for n in line.split()] for line in f.readlines()]
            model.masks.append(np.array(mask))

    # Add rules
    model.rules = [
        Rule(mask=model.masks[0], limits=(0, 17), result=DEATH),
        Rule(mask=model.masks[0], limits=(40, 42), result=LIFE),
        Rule(mask=model.masks[1], limits=(10, 13), result=LIFE),
        Rule(mask=model.masks[2], limits=(9, 21), result=DEATH),
        Rule(mask=model.masks[3], limits=(78, 89), result=DEATH),
        Rule(mask=model.masks[3], limits=(108, None), result=DEATH),
    ]

    view = MncaView(model=model)
    view.edit_traits(kind="livemodal")
