# -*- coding: utf-8 -*-
import inspect


class KernelGroup:
    def __init__(self, collector, coupl, nf, ihq, fonll, nc):
        self.collector = collector
        self.coupl = coupl
        self.nf = nf
        self.ihq = ihq
        self.fonll = fonll
        self.nc = nc

    def __call__(self, esf):
        sig = inspect.signature(self.collector)
        return self.collector(
            esf, **{k: getattr(self, k) for k in sig.parameters if k != "esf"}
        )


def kernel_group(coupl, fonll=False):
    def decorator(collector):
        def make_kernel_group(nf, ihq, nc):
            return KernelGroup(collector, coupl, nf, ihq, fonll, nc)

        return make_kernel_group

    return decorator


@kernel_group("light")
def generate(esf, nf):
    print(esf)
    print(nf)
