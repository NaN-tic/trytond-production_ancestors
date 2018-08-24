#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
from trytond.model import ModelSQL, fields
from trytond.pool import PoolMeta

__all__ = ['Production', 'ProductionParentChild', 'ProductionAncestorSuccessor']


class Production(metaclass=PoolMeta):
    __name__ = 'production'
    parents = fields.Many2Many('production.parent_child', 'child', 'parent',
        'Parents', readonly=True)
    children = fields.Many2Many('production.parent_child', 'parent', 'child',
        'Children', readonly=True)
    ancestors = fields.Many2Many('production.ancestor_successor', 'successor',
        'ancestor', 'Ancestors', readonly=True)
    successors = fields.Many2Many('production.ancestor_successor', 'ancestor',
        'successor', 'Successors', readonly=True)
    parents_char = fields.Function(fields.Char('Parents'), 'get_chars',
        searcher='search_chars')
    ancestors_char = fields.Function(fields.Char('Ancestors'), 'get_chars',
        searcher='search_chars')

    def get_chars(self, name):
        name = name.split('_')[0]
        return ', '.join([p.number for p in getattr(self, name)])

    @classmethod
    def search_chars(cls, name, clause):
        name = name.split('_')[0]
        return [(name + '.rec_name',) + tuple(clause)[1:]]

    @classmethod
    def copy(cls, productions, default=None):
        if default is None:
            default = {}
        default = default.copy()
        default['production_parents'] = None
        default['production_children'] = None
        default['production_ancestors'] = None
        default['production_successors'] = None
        return super(Production, cls).copy(productions, default=default)


class ProductionParentChild(ModelSQL):
    'Production Parents Children'
    __name__ = 'production.parent_child'
    parent = fields.Many2One('production', 'Parent', ondelete='CASCADE',
        required=True)
    child = fields.Many2One('production', 'Child', ondelete='CASCADE',
        required=True)


class ProductionAncestorSuccessor(ModelSQL):
    'Production Ancestor Successor'
    __name__ = 'production.ancestor_successor'
    ancestor = fields.Many2One('production', 'Ancestor', ondelete='CASCADE')
    successor = fields.Many2One('production', 'Successor', ondelete='CASCADE')
