import pandas as pd

lo = pd.read_csv("LO.debug", sep="\s+")
nlo = pd.read_csv("NLO.debug", sep="\s+")

nlo_only = nlo.copy()
nlo_only.drop(columns=["ratio"], inplace=True)
nlo_only["yadism"] = nlo["yadism"] - lo["yadism"]
nlo_only["APFEL"] = nlo["APFEL"] - lo["APFEL"]
nlo_only["ratio"] = nlo_only["yadism"] / nlo_only["APFEL"]
nlo_only["NLO / (LO + NLO) [%]"] = nlo_only["APFEL"] / nlo["APFEL"] * 100

print(nlo_only)
