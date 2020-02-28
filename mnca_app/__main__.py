from mnca_app.mnca_model import MncaModel
from mnca_app.mnca_view import MncaView
from mnca_app.rule import Rule, LIFE, DEATH


def main():
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
