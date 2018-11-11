from ..configuration import BaseConfiguration
from .constants import (DEFAULT_BACKEND, DEFAULT_BOX, DEFAULT_FLAVOUR,
                        DEFAULT_NETWORKS, DEFAULT_USER, FLAVOURS)
from .schema import SCHEMA


class Configuration(BaseConfiguration):

    _SCHEMA = SCHEMA

    def __init__(self):
        super().__init__()
        # top level atttributes
        self.resources = None
        self.backend = DEFAULT_BACKEND
        self.user = DEFAULT_USER
        self.box = DEFAULT_BOX

        self._machine_cls = MachineConfiguration

    @classmethod
    def from_dictionnary(cls, dictionnary, validate=True):
        if validate:
            cls.validate(dictionnary)

        self = cls()
        _resources = dictionnary["resources"]
        _machines = _resources["machines"]
        self.machines = [MachineConfiguration.from_dictionnary(m) for m in
                         _machines]
        for key in ["backend", "user", "box"]:
            value = dictionnary.get(key)
            if value is not None:
                setattr(self, key, value)

        self.finalize()
        return self

    def to_dict(self):
        d = {}
        d.update(backend=self.backend,
                 user=self.user,
                 box=self.box,
                 resources={
                     "machines": [m.to_dict() for m in self.machines]
                 })
        return d


class MachineConfiguration:

    def __init__(self, *,
                 roles=None,
                 flavour=None,
                 number=1,
                 networks=DEFAULT_NETWORKS):
        self.roles = roles

        if flavour is None:
            self.flavour = DEFAULT_FLAVOUR
        if isinstance(flavour, dict):
            self.flavour = flavour
        elif isinstance(flavour, str):
            self.flavour = FLAVOURS[flavour]
        else:
            self.flavour = DEFAULT_FLAVOUR

        self.number = number
        self.networks = networks

    @classmethod
    def from_dictionnary(cls, dictionnary):
        kwargs = {}
        roles = dictionnary["roles"]
        kwargs.update(roles=roles)
        flavour = dictionnary.get("flavour")
        if flavour is not None:
            # The flavour name is used in the dictionnary
            # This makes a diff with the constructor where
            # A dict describing the flavour is given
            kwargs.update(flavour=FLAVOURS[flavour])
        number = dictionnary.get("number")
        if number is not None:
            kwargs.update(number=number)
        networks = dictionnary.get("networks")
        if networks is not None:
            kwargs.update(networks=networks)

        return cls(**kwargs)

    def to_dict(self):
        d = {}
        d.update(roles=self.roles, flavour=self.flavour, number=self.number,
                 networks=self.networks)
        return d
