import random

import numpy as np
from scipy.ndimage import convolve

from traits.api import (
    Array,
    Bool,
    HasRequiredTraits,
    Range,
    Float,
    Dict,
    List,
    on_trait_change,
    Tuple,
    Unicode,
)

from mnca_app.rule import Rule, LIFE, DEATH

RANDOM = "Random"
ZEROS = "Zeros"


class MncaModel(HasRequiredTraits):

    #: Board size (X, Y)
    board_size = Tuple(Range(1, 500), Range(1, 500), required=True)

    #: % of living cells on reset
    reset_life_pct = Float(0.5)

    #: Board for the MNCA
    board = Array(shape=(None, None))

    #: Available masks (name to array)
    masks = Dict(Unicode, Array(shape=(None, None)))

    #: Rules
    rules = List(Rule, required=False)

    #: Pause updating the model
    paused = Bool(False)

    @on_trait_change("board_size")
    def reset_board(self):
        self.board = np.ones(self.board_size, dtype=int)
        self.board_reset()

    def randomize_rules(self):
        rules = []
        print("----------")
        print("New Rules:")
        for i in range(random.randint(2, 10)):
            m = random.randint(0, len(self.masks)-1)
            mask = self.masks[m]

            r_a, r_b = (
                random.randint(0, np.sum(mask)),
                random.randint(0, (np.sum(mask)))
            )
            lower = min([r_a, r_b])
            upper = max([r_a, r_b])

            result = random.choice([DEATH, LIFE])

            rules.append(Rule(mask=mask, limits=(lower, upper), result=result))
            print(f"Rule(mask=masks[{m}], limits=({lower}, {upper}), result={result})")
        print("----------")

        self.rules = rules

    def board_reset(self):
        for i in range(self.board_size[0]):
            for j in range(self.board_size[1]):
                self.board[i, j] = 1 if random.random() < self.reset_life_pct else 0

    def evolve_board(self):
        """
        Evolve the board one step according to the rules
        """
        if self.paused:
            return

        # TODO: update this in another thread if possible, to stop the UI from juttering

        gridmask = np.ones_like(self.board)
        convgrid = np.zeros_like(self.board)

        # Where the lower and upper bounds of the rule are satisfied
        rule1 = np.ones_like(self.board)
        rule2 = np.ones_like(self.board)

        for rule in self.rules:
            if not gridmask.any():
                break
            convolve(self.board, self.masks[rule.mask], mode="wrap", output=convgrid)
            if rule.limits[0] is not None:
                rule1 = np.where(convgrid >= rule.limits[0], 1, 0)
            else:
                rule1[:] = 1

            if rule.limits[1] is not None:
                rule2 = np.where(convgrid <= rule.limits[1], 1, 0)
            else:
                rule2[:] = 1

            slc = (rule1 & rule2 & gridmask)

            self.board[np.where(slc)] = 1 if rule.result == LIFE else 0
            gridmask[np.where(slc)] = 0
