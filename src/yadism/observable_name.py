# -*- coding: utf-8 -*-

kinds = ["F2", "FL"]
# external flavors:
heavys = ["charm", "bottom", "top"]
asys = [h + "asy" for h in heavys]
external_flavors = heavys + ["light", "total"] + asys
# internally we allow in addition for the flavor families
flavor_families = ["asy", "heavy"]
flavors = external_flavors + flavor_families


class ObservableName:
    """
        Wrapper to observable names to easy split them into two parts.

        Parameters
        ----------
            name : str
                full observable name
    """

    def __init__(self, name):
        self.kind = name[:2]
        if self.kind not in kinds:
            raise ValueError(f"Unknown kind {self.kind}")
        self.flavor = name[2:]
        if self.flavor not in flavors:
            raise ValueError(f"Unknown flavor {self.flavor}")

    @property
    def name(self):
        """joint name"""
        return self.kind + self.flavor

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
        return type(self)(kind + self.flavor)

    def apply_asy(self):
        """
            Computes the asymptotic heavy correspondend.

            Returns
            -------
                apply_asy : type(self)
                    asymptotic heavy correspondend
        """
        if self.flavor not in heavys:
            raise ValueError(f"observable is not heavy! [{self}]")
        return self.apply_flavor(self.flavor + "asy")

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
        return type(self)(self.kind + flavor)

    @property
    def is_heavy(self):
        """
            Is it a heavy flavor?

            Returns
            -------
                is_heavy : bool
                    is a heavy flavor?
        """
        return not self.flavor == "light"

    @property
    def is_raw_heavy(self):
        """Is it a raw heavy flavor? i.e. charm, bottom, or, top"""
        return self.flavor in heavys

    @property
    def is_asy(self):
        """Is it a asymptotic raw heavy flavor? i.e. charmasy, bottomasy, or, topasy"""
        return self.flavor in asys

    @property
    def is_composed(self):
        """Is it a composed flavor? i.e. total"""
        return self.flavor == "total"

    @property
    def flavor_family(self):
        """Abstract flavor family name"""
        if self.is_raw_heavy:
            return "heavy"
        if self.is_asy:
            return "asy"
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
        if self.is_asy:
            idx = asys.index(self.flavor)
        else:
            idx = heavys.index(self.flavor)
        return 4 + idx

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

    @classmethod
    def all(cls):
        """
            Iterates all valid (external) names.

            Yields
            ------
                all : cls
                    ObservableName
        """
        for kind in kinds:
            for flav in external_flavors:
                yield cls(kind + flav)
