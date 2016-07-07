#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
from trytond.pool import PoolMeta, Pool

__all__ = ['Reservation']


class Reservation:
    __name__ = 'stock.reservation'
    __metaclass__ = PoolMeta

    @classmethod
    def generate_reservations(cls, clean=True):
        '''Find and relate ancestors and parents when source/destination
        reservations are productions'''
        Production = Pool().get('production')

        reservations = super(Reservation, cls).generate_reservations(clean)

        if not reservations:
            return reservations

        def __get_recursive_productions(productions, parents_update, child_update):
            for reservation in cls.search([
                    ('destination_document', 'in', productions),
                    ]):
                source = reservation.source_document
                if source and source.__name__ == 'production':
                    destination = reservation.destination_document
                    parents_update.setdefault(source, set()).add(destination)
                    child_update.setdefault(destination, set()).add(source)

                    parents_update, child_update = __get_recursive_productions(
                        [source], parents_update, child_update)

            return parents_update, child_update

        sources = set()
        destinations = set()
        productions = set()
        for reservation in reservations:
            source = reservation.source_document
            destination = reservation.destination_document
            if (source and source.__name__ == 'production'):
                sources.add(source)
                productions.add(source)
            if (destination and destination.__name__ == 'production'):
                destinations.add(destination)
                productions.add(destination)
        
        parents_update = {}
        child_update = {}
        for production in productions:
            parents_update[production] = set()
            child_update[production] = set()

        # call recursive from main production to last childreen production
        parents_update, child_update = __get_recursive_productions(
            list(destinations - sources), parents_update, child_update)

        to_write = []
        for k, v in parents_update.iteritems():
            to_write.extend(([k], {
                'production_parents': [('add', [p.id for p in v])],
                }))
        for k, v in child_update.iteritems():
            to_write.extend(([k], {
                'production_childrens': [('add', [p.id for p in v])],
                }))
        if to_write:
            Production.write(*to_write)

        return reservations
