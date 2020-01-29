import numpy as np
from traits.api import Instance
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

    def default_traits_view(self):
        view = View(
            HSplit(
                UItem(
                    "model.board",
                    editor=BoolArrayEditor(
                        scale=True,
                        allow_upscaling=False,
                        allow_clipping=True,
                        update_ms=600,
                    ),
                ),
                VGroup(
                    Item("model.paused", label="Pause"),
                    Item("model.board_size"),
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
    mask_files = ["mask_a.txt", "mask_b.txt", "mask_c.txt", "mask_d.txt",]
    masks = []
    for m_file in mask_files:
        with open(os.path.join("mnca_app", "data", "masks", m_file), "r") as f:
            mask = [[int(n) for n in line.split()] for line in f.readlines()]
            masks.append(np.array(mask))
    #model.rules = [
    #    Rule(mask=masks[2], limits=(38, 53), result=DEATH),
    #    Rule(mask=masks[0], limits=(8, 60), result=LIFE),
    #    Rule(mask=masks[3], limits=(53, 68), result=DEATH),
    #    Rule(mask=masks[2], limits=(45, 97), result=DEATH),
    #    Rule(mask=masks[3], limits=(12, 54), result=LIFE),
    #    Rule(mask=masks[2], limits=(0, 15), result=DEATH),
    #]
    model.rules = [
        Rule(mask=masks[0], limits=(0, 17), result=DEATH),
        Rule(mask=masks[0], limits=(40, 42), result=LIFE),
        Rule(mask=masks[1], limits=(10, 13), result=LIFE),
        Rule(mask=masks[2], limits=(9, 21), result=DEATH),
        Rule(mask=masks[3], limits=(78, 89), result=DEATH),
        Rule(mask=masks[3], limits=(108, None), result=DEATH),
    ]

    view = MncaView(model=model)
    view.edit_traits(kind="livemodal")
