import dataclasses

import rich
from rich import align, box, table
from rich.console import Group
from rich.panel import Panel


class Scheme(dict):
    def __init__(self, args):
        self.args = args
        for k, v in vars(args).items():
            if k[0] == "m" and len(k) == 2:
                v = "FONLL" if v else "ZM-VFNS"
            self[k] = v

    @property
    def masses(self):
        ms = {}
        for i, q in enumerate("cbt"):
            ms[i + 4] = getattr(self.args, f"m{q}")

        return ms

    def render(self):
        ms = "    ".join(
            [f"[yellow]{k}[/]: [green]{v}[/]" for k, v in self.items() if k != "obs"]
        )
        return Group(
            ms, align.Align(f"Observable: [b cyan]F{self['obs']}", align="center")
        )


class ObservableName:
    def __init__(self, name):
        self.name = name

    @property
    def family(self):
        if "total" in self.name:
            return "total"
        if "light" in self.name:
            return "light"
        return "heavy"

    @property
    def hq(self):
        if self.name in ["light", "total"]:
            return 0
        return ["charm", "bottom", "top"].index(self.name) + 4


kg_space = dict(
    nf=[3, 4, 5, 6],
    coupl=["light", "heavy", "miss"],
    ihq=[0, 4, 5, 6],
    fonll=[False, True],
)


@dataclasses.dataclass
class KernelGroup:
    coupl: str
    nf: int
    ihq: int = 0
    fonll: bool = False
    nc: int = 0

    @property
    def flav(self):
        if self.ihq == 0:
            return ""
        return "cbt"[self.ihq - 4]

    def __repr__(self):
        for name, domain in kg_space.items():
            attr = getattr(self, name)
            if attr not in domain:
                raise RuntimeError(f"'{name}={attr}' not in domain {domain}")

        attributes = []

        if self.ihq != 0:
            # heavylight is allowed
            if self.coupl != "light" and self.nf >= self.ihq:
                if not self.fonll:
                    raise RuntimeError(
                        f"'ihq={self.ihq}' is light when {self.nf} flavors are active"
                    )
                if self.nf > self.ihq:
                    raise RuntimeError(
                        f"'ihq={self.ihq}' is light when {self.nf} flavors "
                        "are active (even with FONLL)"
                    )

        if self.fonll:
            self.ihq = self.nf

        if self.ihq < self.nf or (self.ihq == self.nf and not self.fonll):
            heavyness = f"zm:{self.nf}"
        elif not self.fonll:
            heavyness = f"{self.nf}f:{self.flav}"
        else:
            heavyness = f"FO:{self.flav}"
        attributes.append(heavyness)

        if self.coupl == "miss":
            if self.ihq == 0:
                raise RuntimeError(
                    "Missing does not make sense for a pure light kernel."
                )
            attributes.append(f"/{self.flav}")

        if self.nc == 0:
            self.nc = self.nf
        elif self.nc == 1:
            attributes.append(f"~~{'cbt'[self.ihq-4]}")
        else:
            attributes.append(f"~~{self.nc}")

        attributes = ", ".join(attributes)
        return f"F{self.coupl}({attributes})"


class Component(list):
    heavyness = {0: "light", 4: "charm", 5: "bottom", 6: "top"}

    def __init__(self, heavy, kernels=None):
        self.heavy = heavy
        self.name = "F" + self.heavyness[heavy]

        if kernels is None:
            kernels = []
        self.extend(kernels)

    def render(self, color="magenta", color_add="none"):
        return f"[{color}]{self.name}[/] = " + " + ".join(
            [f"[{color_add}]{kg}[/]" for kg in self]
        )


class Patch(list):
    def __init__(self, obs, nf, components=None):
        self.obs = obs
        self.nf = nf

        if components is None:
            components = []
        self.extend(components)

    def render(self):
        lines = [comp.render() for comp in self]
        obs = Component(0, [comp.name for comp in self])
        obs.name = "F" + self.obs
        lines.append(obs.render(color="cyan", color_add="magenta"))

        return Group(*lines)


class VFNS(list):
    def __init__(self, confs, patches=None):
        self.scheme = Scheme(confs)
        self.obs = ObservableName(confs.obs)

        if patches is None:
            patches = []
        self.extend(patches)

    @property
    def masses(self):
        return self.scheme.masses

    def render(self):
        tab = table.Table.grid()

        tab.add_column(justify="right")
        tab.add_column()

        for patch in self:
            flavors = Panel.fit(
                f"[i]active flavors:[/] [red]{patch.nf}", box=box.SQUARE
            )
            side = patch.nf % 2
            for content in (flavors, patch.render()):
                row = [""]
                row.insert(
                    side, align.Align(content, align="right" if side == 0 else "left")
                )

                tab.add_row(*row)

        rich.print(
            align.Align(
                Panel(self.scheme.render(), box=box.HORIZONTALS), align="center"
            ),
            "\n",
            align.Align(tab, align="center"),
        )
