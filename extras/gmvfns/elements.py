import dataclasses

import rich
from rich import align, box, table
from rich.console import Group
from rich.panel import Panel


class Scheme(dict):
    def __init__(self, args):
        for k, v in vars(args).items():
            if k[0] == "m" and len(k) == 2:
                v = "FONLL" if v else "ZM-VFNS"
            self[k] = v

    def render(self):
        ms = "    ".join(
            [f"[yellow]{k}[/]: [green]{v}[/]" for k, v in self.items() if k != "obs"]
        )
        return Group(
            ms, align.Align(f"Observable: [b cyan]F{self['obs']}", align="center")
        )


@dataclasses.dataclass
class KernelGroup:
    nf: int
    ihq: int = 0
    missing: bool = False

    @property
    def flav(self):
        if self.ihq == 0:
            return ""
        return "cbt"[self.ihq - 4]

    def __repr__(self):
        heavyness = f"zm:{self.nf}"
        if self.ihq != 0:
            heavyness = f"{self.nf}{self.flav}"

        missing = ""
        if self.missing:
            if self.ihq == 0:
                raise RuntimeError(
                    "Missing does not make sense for a pure light kernel."
                )
            missing = f", /{self.flav}"

        return f"F({heavyness}{missing})"


class Component(list):
    def __init__(self, kind, kernels=None):
        self.kind = kind

        if kernels is None:
            kernels = []
        self.extend(kernels)

    @property
    def name(self):
        return f"F{self.kind}"

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
        lines.insert(
            0, Panel.fit(f"[i]active flavors:[/] [red]{self.nf}", box=box.SQUARE)
        )
        lines.append(
            Component(self.obs, [comp.name for comp in self]).render(
                color="cyan", color_add="magenta"
            )
        )

        return Group(*lines)


class VFNS(list):
    def __init__(self, confs, patches=None):
        self.scheme = Scheme(confs)

        if patches is None:
            patches = []
        self.extend(patches)

    def render(self):
        tab = table.Table.grid()

        tab.add_column(justify="right")
        tab.add_column()

        for patch in self:
            row = [""]
            row.insert(patch.nf % 2, patch.render())

            tab.add_row(*row)

        rich.print(
            align.Align(
                Panel(self.scheme.render(), box=box.HORIZONTALS), align="center"
            ),
            align.Align(tab, align="center"),
        )
