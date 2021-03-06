from abc import abstractmethod
from copy import deepcopy

from Pyllurium.Particle import Particle
from Pyllurium.SubAtomic import Neutron, Proton, Electron
from Pyllurium.ElectronCloud import ElectronCloud


class Atom(Particle):
    def __init__(self):
        self.neutrons = [Neutron(parent=self) for _ in range(self.num_neutrons)]
        self.protons = [Proton(parent=self) for _ in range(self.num_protons)]

        self.electron_cloud = ElectronCloud([Electron(parent=self) for _ in range(self.num_electrons)])

    @property
    def num_neutrons(self):
        return round(self.mass) - self.num_protons

    @property
    def num_electrons(self):
        return self.num_protons

    @property
    def num_protons(self):
        return type(self)._num_protons

    @property
    @abstractmethod
    def _num_protons(self):
        pass

    @property
    def mass(self):
        return type(self)._mass

    @property
    @abstractmethod
    def _mass(self):
        pass

    @property
    def symbol(self):
        return type(self)._symbol

    @property
    @abstractmethod
    def _symbol(self):
        pass

    @property
    def charge(self):
        return sum(subatomic.charge for subatomic in self.neutrons + self.protons + self.electron_cloud.electrons)

    @property
    def electron_configuration(self):
        return ''.join(repr(orbital) for orbital in self.electron_cloud.orbitals)

    @property
    def name(self):
        return type(self).__name__

    def __add__(self, other):
        from Pyllurium import Compound
        return Compound(self, other)

    def __mul__(self, other):
        from Pyllurium import Compound
        return Compound(*(deepcopy(self) for _ in range(other)))
