#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
from trytond.pool import PoolMeta, Pool

__all__ = ['Reservation']


class Reservation:
    __name__ = 'stock.reservation'
    __metaclass__ = PoolMeta

    @classmethod
    def generate_reservations(cls, clean=True):
        pool = Pool()
        Production = pool.get('production')
        ParentChild = pool.get('production.parent_child')
        AncestorSuccessor = pool.get('production.ancestor_successor')

        reservations = super(Reservation, cls).generate_reservations(clean)

        # Clear all relationships
        ParentChild.delete(ParentChild.search([]))
        AncestorSuccessor.delete(AncestorSuccessor.search([]))

        ancestors = set(Production.search([
                ('state', 'not in', ['cancel', 'done']),
                ]))

        # If clean was set to False, then 'reservations' variable will not
        # contain all the records so we must search() here.
        for reservation in cls.search([]):
            source = reservation.source_document
            if not source or not source.__name__ == 'production':
                continue
            destination = reservation.destination_document
            if (destination and destination.__name__ == 'production'
                    and source in ancestors):
                ancestors.remove(source)

        parents_update = {}
        ancestors_update = {}
        ancestors = [x.id for x in ancestors]
        for ancestor in ancestors:
            parents_update[ancestor] = set([ancestor])
            ancestors_update[ancestor] = set([ancestor])

        parents = ancestors
        processed = set()
        exit = False
        while not exit:
            exit = True
            # Discard already processed productions to try to avoid rare
            # infinite loops
            pending = set(parents) - processed
            processed |= set(parents)
            children = []
            for reservation in cls.search([
                        ('destination_document', 'in',
                            ['production,%d' % x for x in pending]),
                        ]):
                source = reservation.source_document
                destination = reservation.destination_document
                if source and source.__name__ == 'production':
                    exit = False
                    destination = reservation.destination_document
                    if not source.id in parents_update:
                        parents_update[source.id] = set()
                        ancestors_update[source.id] = set()
                    parents_update[source.id].add(destination.id)
                    ancestors_update[source.id] |= ancestors_update[
                        destination.id]
                    children.append(source.id)
            parents = children

        if parents_update:
            to_update = []
            for production_id in parents_update.keys():
                to_update.append([Production(production_id)])
                parents = list(parents_update[production_id])
                ancestors = list(ancestors_update[production_id])
                to_update.append({
                        'parents': [('add', parents)],
                        'ancestors': [('add', ancestors)],
                        })
            Production.write(*to_update)
        return reservations
