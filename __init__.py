# This file is part production_ancestors module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from . import production


def register():
    Pool.register(
        production.Production,
        production.ProductionParentChild,
        production.ProductionAncestorSuccessor,
        module='production_ancestors', type_='model')
