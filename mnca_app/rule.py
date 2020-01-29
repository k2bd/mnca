import numpy as np

from traits.api import (
    Array,
    Either,
    Enum,
    HasRequiredTraits,
    Int,
    Tuple,
)

LIFE = "Life"
DEATH = "Death"
PASS = "Pass"


class Rule(HasRequiredTraits):
    # Mask the rule applies to
    mask = Array(shape=(None, None), required=True)

    #: Rule limits (inclusive!), or None if there is no bound
    #: TODO: limits should match dtype if we want continuous MNCAs
    limits = Tuple(Either(Int, None), Either(Int, None), required=True)

    result = Enum(LIFE, DEATH, required=True)