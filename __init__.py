# This file is part production_ancestors module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from .production import *
from .stock import *

def register():
    Pool.register(
        Production,
        ProductionParentChild,
        ProductionAncestorSuccessor,
        Reservation,
        module='production_ancestors', type_='model')
