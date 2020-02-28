from traits.api import (
    Either,
    Enum,
    HasRequiredTraits,
    Int,
    Unicode,
)

LIFE = "Life"
DEATH = "Death"
PASS = "Pass"
BOTH = "Both"


class Rule(HasRequiredTraits):
    # Mask the rule applies to
    mask = Unicode(required=True)

    #: Whether this rule acts on living or dead cells, or both
    acts_on = Enum(BOTH, (1, 0, BOTH))

    #: Rule limits (inclusive!), or None if there is no bound
    #: TODO: limits should match dtype if we want continuous MNCAs
    lower_limit = Either(Int, None, required=True)
    upper_limit = Either(Int, None, required=True)

    result = Enum(LIFE, DEATH, required=True)
