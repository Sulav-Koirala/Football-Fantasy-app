class PlayerAlreadyInTeamException(Exception):
    pass

class MaximumPlayerLimit(Exception):
    pass

class SlotAlreadyTakenError(Exception):
    pass

class SlotMismatchError(Exception):
    pass

class PlayerNotInTeamError(Exception):
    pass

class TransferError(Exception):
    pass

class PlayerPositionMismatchError(Exception):
    pass

class RolesAlreadyAssignedError(Exception):
    pass

class DoubleRoleError(Exception):
    pass