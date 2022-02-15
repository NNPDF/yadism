# -*- coding: utf-8 -*-
from banana.data.db import Base
from sqlalchemy import Column, Integer, Text


class Observable(Base):
    __tablename__ = "observables"

    PolarizationDIS = Column(Integer)
    ProjectileDIS = Column(Text)
    PropagatorCorrection = Column(Integer)
    interpolation_is_log = Column(Text)
    interpolation_polynomial_degree = Column(Integer)
    interpolation_xgrid = Column(Text)
    observables = Column(Text)
    prDIS = Column(Text)
    TargetDIS = Column(Text)
