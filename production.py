#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
from trytond.model import ModelSQL, fields
from trytond.pool import PoolMeta

__all__ = ['Production', 'ProductionParent', 'ProductionChild']


class Production:
    __name__ = 'production'
    __metaclass__ = PoolMeta
    # production_parents = fields.Char('Production Parents', readonly=True)
    # production_childrens = fields.Char('Production Childrens', readonly=True)
    production_parents = fields.Many2Many('production.parent',
        'production', 'parent', 'Parents', readonly=True)
    production_childrens = fields.Many2Many('production.child',
        'production', 'child', 'Childrens', readonly=True)
    production_parents_char = fields.Function(fields.Char('Parents'),
        'get_production_parents')
    production_childrens_char = fields.Function(fields.Char('Childens'),
        'get_production_children')

    def get_production_parents(self, name):
        return ', '.join([p.code for p in self.production_parents])

    def get_production_children(self, name):
        return ', '.join([p.code for p in self.production_childrens])

    @classmethod
    def copy(cls, productions, default=None):
        if default is None:
            default = {}
        default = default.copy()
        default['production_parents'] = None
        default['production_childrens'] = None
        return super(Production, cls).copy(productions, default=default)


class ProductionParent(ModelSQL):
    'Production - Parent'
    __name__ = 'production.parent'
    production = fields.Many2One('production', 'Production', ondelete='CASCADE',
        required=True, select=True)
    parent = fields.Many2One('production', 'Parent', ondelete='CASCADE',
        required=True, select=True)


class ProductionChild(ModelSQL):
    'Production - Child'
    __name__ = 'production.child'
    production = fields.Many2One('production', 'Production', ondelete='CASCADE',
        required=True, select=True)
    child = fields.Many2One('production', 'Child', ondelete='CASCADE',
        required=True, select=True)
