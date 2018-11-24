from Pyllurium.utils import SUP


def get_orbitals():
    madelung = 1

    combinations = [
        SubLevel(shell_num, madelung - shell_num)
        for shell_num in range(1, madelung + 1) if madelung - shell_num < shell_num and madelung - shell_num <= 3
    ]

    while True:
        for combination in combinations:
            yield combination

        madelung += 1

        combinations = [
            SubLevel(shell_num, madelung - shell_num)
            for shell_num in range(1, madelung + 1) if madelung - shell_num < shell_num and madelung - shell_num <= 3
        ]


class SubLevel(list):
    def __init__(self, principal_number, azimuthal_number):
        super().__init__()

        self.principal_number = principal_number
        self.azimuthal_number = azimuthal_number

    @property
    def maxE(self):
        return 2 + self.azimuthal_number * 4

    def __repr__(self):
        return (
            str(self.principal_number) +
            ('s', 'p', 'd', 'f')[self.azimuthal_number] +
            str(len(self)).translate(SUP)
        )


class ElectronCloud:
    def __init__(self, electrons):
        self.electrons = electrons

    @property
    def orbitals(self):
        orbitals = []

        orbital_generator = get_orbitals()

        current_orbital = next(orbital_generator)
        orbitals.append(current_orbital)

        for electron in self.electrons:
            if len(current_orbital) == current_orbital.maxE:
                current_orbital = next(orbital_generator)
                orbitals.append(current_orbital)

            current_orbital.append(electron)

        return orbitals
