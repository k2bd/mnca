import pkg_resources
import random

import numpy as np
from scipy.ndimage import convolve

from traits.api import (
    Array,
    Bool,
    Color,
    Dict,
    Directory,
    Float,
    HasRequiredTraits,
    Instance,
    List,
    on_trait_change,
    Range,
    Tuple,
    Unicode,
)

from mnca_app.mask import load_masks
from mnca_app.rule import Rule, LIFE, DEATH, BOTH

DEFAULT_MASKS_DIR = pkg_resources.resource_filename("mnca_app", "data/masks")

RANDOM = "Random"
ZEROS = "Zeros"


DEFAULT_BRUSH = np.array(
    [
        [0, 0, 1, 1, 1, 0, 0],
        [0, 1, 1, 1, 1, 1, 0],
        [1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1],
        [0, 1, 1, 1, 1, 1, 0],
        [0, 0, 1, 1, 1, 0, 0],
    ],
)


class MncaModel(HasRequiredTraits):

    #: Board size (X, Y)
    board_size = Tuple(Range(1, 500), Range(1, 500), required=True)

    #: % of living cells on reset
    reset_life_pct = Float(0.5)

    #: Board for the MNCA
    board = Array(shape=(None, None))

    #: Directory to parse masks from
    masks_dir = Directory(DEFAULT_MASKS_DIR, exists=True)

    #: Available masks (name to array)
    masks = Dict(Unicode, Array(shape=(None, None)))

    #: Rules
    rules = List(Instance(Rule), required=False)

    #: Pause updating the model
    paused = Bool(False)

    #: Drawing brush
    brush = Array(shape=(None, None), value=DEFAULT_BRUSH)

    live_color = Color("white")
    dead_color = Color("black")

    @on_trait_change("masks_dir")
    def set_masks(self):
        self.masks = load_masks(self.masks_dir)
        self.randomize_rules()

    def _masks_default(self):
        # TODO: this is a bit hacky to help with traits init of this class
        return load_masks(DEFAULT_MASKS_DIR)

    @on_trait_change("board_size")
    def reset_board(self):
        self.board = np.ones(self.board_size, dtype=int)
        self.board_reset()

    @on_trait_change("rules[]")
    def print_new_rules(self):
        print("----------")
        for rule in self.rules:
            print(
                "mask='{rule.mask}', "
                "acts_on={rule.acts_on!r}, "
                "lower_limit={rule.lower_limit}, "
                "upper_limit={rule.upper_limit}, "
                "result={rule.result})".format(rule=rule)
            )

    def randomize_rules(self):
        rules = []
        for i in range(random.randint(2, 10)):
            mask_name = random.choice(list(self.masks.keys()))
            mask = self.masks[mask_name]

            r_a, r_b = (
                random.randint(0, np.sum(mask)),
                random.randint(0, (np.sum(mask)))
            )
            lower = min([r_a, r_b])
            upper = max([r_a, r_b])

            acts_on = random.choice([0, 1, BOTH])

            result = random.choice([DEATH, LIFE])

            rules.append(
                Rule(
                    mask=mask_name,
                    lower_limit=lower,
                    upper_limit=upper,
                    acts_on=acts_on,
                    result=result
                )
            )

        self.rules = rules

    def board_reset(self):
        for i in range(self.board_size[0]):
            for j in range(self.board_size[1]):
                self.board[i, j] = 1 if random.random() < self.reset_life_pct else 0

    def clear_board(self, value=0):
        self.board[:, :] = value

    def draw(self, target):
        """
        Draw on the board using the current brush at the target coordinates
        """
        for offset in np.transpose(np.where(self.brush)):
            offset -= np.array(self.brush.shape) // 2
            coord = target + offset
            if coord[0] < self.board.shape[0] and coord[1] < self.board.shape[1]:
                self.board[coord[0], coord[1]] = 1

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
            if rule.lower_limit is not None:
                rule1 = np.where(convgrid >= rule.lower_limit, 1, 0)
            else:
                rule1[:] = 1

            if rule.upper_limit is not None:
                rule2 = np.where(convgrid <= rule.upper_limit, 1, 0)
            else:
                rule2[:] = 1

            slc = (rule1 & rule2 & gridmask)

            if rule.acts_on != BOTH:
                acts_on = np.where(self.board == rule.acts_on, 1, 0)
                slc &= acts_on

            self.board[np.where(slc)] = 1 if rule.result == LIFE else 0
            gridmask[np.where(slc)] = 0
