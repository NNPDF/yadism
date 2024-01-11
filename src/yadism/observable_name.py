fake_kind = "??"
sfs = ["F2", "FL", "F3", "g1", "gL", "g4"]
# xs = ["XSreduced", "XSyreduced"]
xs = [
    "XSHERANC",
    "XSHERANCAVG",
    "XSHERACC",
    "XSCHORUSCC",
    "XSNUTEVCC",
    "XSNUTEVNU",
    "FW",
    "F1",
    "g5",
    "XSFPFCC",
]
kinds = sfs + xs + [fake_kind]
# external flavors:
heavys = ["charm", "bottom", "top"]
heavylights = [h + "light" for h in heavys]
external_flavors = heavys + ["light", "total"] + heavylights
# internally we allow in addition for the flavor families
flavors = external_flavors + ["heavy"]


class ObservableName:
    """
    Wrapper to observable names to easy split them into two parts.

    Parameters
    ----------
        name : str
            full observable name
    """

    def __init__(self, name):
        p = name.split("_")
        if len(p) == 1:
            self.kind, self.flavor = p[0], "total"
        elif len(p) == 2:
            self.kind, self.flavor = p[0], p[1]
        else:
            raise ValueError(f"Unknown obsname {name}")
        if self.kind not in kinds:
            raise ValueError(f"Unknown kind {self.kind}")
        if self.flavor not in flavors:
            raise ValueError(f"Unknown flavor {self.flavor}")

    @property
    def name(self):
        """joint name"""
        return self.kind + "_" + self.flavor

    @property
    def is_parity_violating(self):
        """Check if it is a parity violating observable."""
        if self.kind in ["F3", "gL", "g4"]:
            return True
        return False

    def __eq__(self, other):
        """Test equality of kind and flavor"""
        return self.kind == other.kind and self.flavor == other.flavor

    def apply_kind(self, kind):
        """
        Create new object with given kind and our flavor

        Parameters
        ----------
            kind : str
                new kind

        Returns
        -------
            apply_kind : type(self)
                new kind and our flavor
        """
        return type(self)(kind + "_" + self.flavor)

    def __repr__(self):
        """The full name is the representation"""
        return self.name

    def apply_flavor(self, flavor):
        """
        Create new object with given flavor and our kind

        Parameters
        ----------
            flavor : str
                new flavor

        Returns
        -------
            apply_flavor : type(self)
                our kind and new flavor
        """
        return type(self)(self.kind + "_" + flavor)

    @property
    def is_heavy(self):
        """
        Is it a heavy flavor?

        Returns
        -------
            is_heavy : bool
                is a heavy flavor?
        """
        return self.flavor != "light"

    @property
    def is_raw_heavy(self):
        """Is it a raw heavy flavor? i.e. charm, bottom, or, top"""
        return self.flavor in heavys

    @property
    def is_heavylight(self):
        """Is it a heavylight flavor? i.e. charmlight, bottomlight, or, toplight"""
        return self.flavor in heavylights

    @property
    def is_composed(self):
        """Is it a composed flavor? i.e. total"""
        return self.flavor == "total"

    @property
    def flavor_family(self):
        """Abstract flavor family name"""
        if self.is_raw_heavy:
            return "heavy"
        if self.is_heavylight:
            return "light"
        return self.flavor

    def apply_flavor_family(self):
        """
        Return name with abstract flavor family name

        Returns
        -------
            apply_flavor_family : type(self)
                new ObservableName
        """
        return self.apply_flavor(self.flavor_family)

    @property
    def hqnumber(self):
        """Heavy quark flavor number"""
        if self.is_heavylight:
            idx = heavylights.index(self.flavor)
        elif self.flavor_family in ["light", "total"]:
            idx = -4
        else:
            idx = heavys.index(self.flavor)
        return 4 + idx

    @property
    def raw_flavor(self):
        """underlying raw flavor"""
        if self.flavor == "light":
            return self.flavor
        return heavys[self.hqnumber - 4]

    @classmethod
    def has_heavies(cls, names):
        """
        Are there any heavy objects in names?

        Parameters
        ----------
            names : list(str)
                names to check

        Returns
        -------
            has_heavies : bool
                are there heavy obs in names?
        """
        for n in names:
            if not cls.is_valid(n):
                continue
            o = cls(n)
            if o.is_heavy:
                return True
        return False

    @classmethod
    def has_lights(cls, names):
        """
        Are there any light objects in names?

        Parameters
        ----------
            names : list(str)
                names to check

        Returns
        -------
            has_lights : bool
                are there light obs in names?
        """
        for n in names:
            if not cls.is_valid(n):
                continue
            o = cls(n)
            if o.flavor == "light":
                return True
        return False

    @property
    def mass_label(self):
        """Mass label in the theory runcard"""
        if self.flavor == "light":
            return None
        else:
            return f"m{self.flavor[0]}"

    @classmethod
    def is_valid(cls, name):
        """
        Tests whether the name is a valid observable name

        Returns
        -------
            is_valid : bool
                is valid name?
        """
        try:
            cls(name)
            return True
        except ValueError:
            return False
