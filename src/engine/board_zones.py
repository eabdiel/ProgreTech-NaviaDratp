class BoardZones:
    """Shared board-zone definitions.

    Coordinates are row, col.
    """

    SUMMON_SQUARES = {
        1: [(6, 0), (6, 1), (6, 2), (6, 4), (6, 5), (6, 6), (5, 0), (5, 6)],
        2: [(0, 0), (0, 1), (0, 2), (0, 4), (0, 5), (0, 6), (1, 0), (1, 6)],
    }

    GRZ_SQUARES = [(3, 1), (3, 2), (3, 3), (3, 4), (3, 5)]

    NAVIA_SQUARES = {
        1: (6, 3),
        2: (0, 3),
    }
