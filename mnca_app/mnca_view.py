import numpy as np
from traits.api import Instance, Button
from traitsui.api import (
    EnumEditor,
    HGroup,
    HSplit,
    Item,
    ModelView,
    ObjectColumn,
    TableEditor,
    TextEditor,
    UItem,
    VGroup,
    View,
    VSplit,
)

from mnca_app.rule import Rule, LIFE, DEATH
from mnca_app.mnca_model import MncaModel
from mnca_app.mnca_board_editor import BoolArrayEditor


def optional_int_editor():
    return TextEditor(
        evaluate=lambda x: int(x) if x != "" else None,
        format_func=lambda x: str(x) if x is not None else "",
    )


class MncaView(ModelView):

    model = Instance(MncaModel, allow_none=False)

    randomize_rules = Button("Randomize Rules")

    def _randomize_rules_fired(self):
        self.model.randomize_rules()

    reset_board = Button("Reset Board")

    def _reset_board_fired(self):
        self.model.reset_board()

    clear_board = Button("Clear Board")

    def _clear_board_fired(self):
        self.model.clear_board()

    def rules_table(self):
        return TableEditor(
            sortable=False,
            auto_size=True,
            orientation="vertical",
            edit_view=View(
                Item("mask", editor=EnumEditor(values=sorted(self.model.masks.keys()))),
                Item("lower_limit", editor=optional_int_editor()),
                Item("upper_limit", editor=optional_int_editor()),
                Item("acts_on"),
                Item("result"),
            ),
            columns=[
                ObjectColumn(
                    name="mask",
                    label="Mask",
                    editable=False,
                ),
                ObjectColumn(
                    name="lower_limit",
                    label="Lower",
                    editable=False,
                ),
                ObjectColumn(
                    name="upper_limit",
                    label="Upper",
                    editable=False,
                ),
                ObjectColumn(
                    name="acts_on",
                    label="Acts On",
                    editable=False,
                ),
                ObjectColumn(
                    name="result",
                    label="Result",
                    editable=False,
                )
            ]
        )

    def default_traits_view(self):
        view = View(
            HSplit(
                VGroup(
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
                    HGroup(
                        Item("model.live_color", label="Life Colour"),
                        Item("model.dead_color", label="Dead Colour"),
                    ),
                ),
                VSplit(
                    VGroup(
                        Item("model.paused", label="Pause"),
                        Item("model.board_size"),
                    ),
                    VGroup(
                        Item("model.reset_life_pct", label="Reset Life %"),
                        UItem("reset_board"),
                        UItem("clear_board"),
                    )
                ),
                VGroup(
                    UItem("model.rules", editor=self.rules_table()),
                    UItem("randomize_rules"),
                ),
                springy=True,
            ),
            resizable=True,
        )
        return view


if __name__ == "__main__":
    # Model with example ruleset
    model = MncaModel(
        board_size=(400, 400),
        rules=[
            Rule(mask="8_neighbor.txt", lower_limit=3, upper_limit=7, result=DEATH),
            Rule(mask="8_neighbor.txt", lower_limit=2, upper_limit=5, result=DEATH),
            Rule(mask="plus_1w1l.txt", lower_limit=1, upper_limit=1, result=DEATH),
            Rule(mask="plus_1w1l.txt", lower_limit=1, upper_limit=4, result=LIFE),
            Rule(mask="9_neighbor.txt", lower_limit=6, upper_limit=9, result=LIFE),
            Rule(mask="plus_1w2l.txt", lower_limit=1, upper_limit=5, result=LIFE),
            Rule(mask="9_neighbor.txt", lower_limit=0, upper_limit=7, result=DEATH),
            Rule(mask="9_neighbor.txt", lower_limit=1, upper_limit=4, result=LIFE),
            Rule(mask="8_neighbor.txt", lower_limit=6, upper_limit=8, result=DEATH),
        ],
    )
    view = MncaView(model=model)
    view.edit_traits(kind="livemodal")
