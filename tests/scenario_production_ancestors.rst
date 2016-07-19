=============================
Production Ancestors Scenario
=============================

=============
General Setup
=============

Imports::

    >>> import datetime
    >>> from dateutil.relativedelta import relativedelta
    >>> from decimal import Decimal
    >>> from proteus import config, Model, Wizard
    >>> from trytond.modules.company.tests.tools import create_company, \
    ...     get_company
    >>> today = datetime.date.today()
    >>> yesterday = today - relativedelta(days=1)

Create database::

    >>> config = config.set_trytond()
    >>> config.pool.test = True

Install production Module::

    >>> Module = Model.get('ir.module')
    >>> modules = Module.find([('name', '=', 'production_ancestors')])
    >>> Module.install([x.id for x in modules], config.context)
    >>> modules = Module.find([('name', '=', 'stock_supply_production')])
    >>> Module.install([x.id for x in modules], config.context)
    >>> Wizard('ir.module.install_upgrade').execute('upgrade')

Create company::

    >>> _ = create_company()
    >>> company = get_company()

Create product::

    >>> ProductUom = Model.get('product.uom')
    >>> unit, = ProductUom.find([('name', '=', 'Unit')])
    >>> ProductTemplate = Model.get('product.template')
    >>> Product = Model.get('product.product')
    >>> product = Product()
    >>> template = ProductTemplate()
    >>> template.name = 'product'
    >>> template.default_uom = unit
    >>> template.type = 'goods'
    >>> template.list_price = Decimal(30)
    >>> template.cost_price = Decimal(20)
    >>> template.save()
    >>> product.template = template
    >>> product.save()

Create Components::

    >>> component1 = Product()
    >>> template1 = ProductTemplate()
    >>> template1.name = 'component 1'
    >>> template1.default_uom = unit
    >>> template1.type = 'goods'
    >>> template1.list_price = Decimal(5)
    >>> template1.cost_price = Decimal(1)
    >>> template1.save()
    >>> component1.template = template1
    >>> component1.save()

    >>> component2 = Product()
    >>> template2 = ProductTemplate()
    >>> template2.name = 'component 2'
    >>> template2.default_uom = unit
    >>> template2.type = 'goods'
    >>> template2.list_price = Decimal(5)
    >>> template2.cost_price = Decimal(1)
    >>> template2.save()
    >>> component2.template = template2
    >>> component2.save()

Create Subcomponents::

    >>> subcomponent1 = Product()
    >>> template3 = ProductTemplate()
    >>> template3.name = 'subcomponent 1'
    >>> template3.default_uom = unit
    >>> template3.type = 'goods'
    >>> template3.list_price = Decimal(5)
    >>> template3.cost_price = Decimal(1)
    >>> template3.save()
    >>> subcomponent1.template = template3
    >>> subcomponent1.save()

    >>> subcomponent2 = Product()
    >>> template4 = ProductTemplate()
    >>> template4.name = 'subcomponent 2'
    >>> template4.default_uom = unit
    >>> template4.type = 'goods'
    >>> template4.list_price = Decimal(5)
    >>> template4.cost_price = Decimal(1)
    >>> template4.save()
    >>> subcomponent2.template = template1
    >>> subcomponent2.save()

Create Bill of Material::

    >>> BOM = Model.get('production.bom')
    >>> BOMInput = Model.get('production.bom.input')
    >>> BOMOutput = Model.get('production.bom.output')
    >>> bom = BOM(name='product')
    >>> input1 = BOMInput()
    >>> bom.inputs.append(input1)
    >>> input1.product = component1
    >>> input1.quantity = 2
    >>> input2 = BOMInput()
    >>> bom.inputs.append(input2)
    >>> input2.product = component2
    >>> input2.quantity = 2
    >>> output = BOMOutput()
    >>> bom.outputs.append(output)
    >>> output.product = product
    >>> output.quantity = 1
    >>> bom.save()

    >>> ProductBom = Model.get('product.product-production.bom')
    >>> product.boms.append(ProductBom(bom=bom))
    >>> product.save()

Create sub Bill of Material::

    >>> subbom = BOM(name='component 1')
    >>> input1 = BOMInput()
    >>> subbom.inputs.append(input1)
    >>> input1.product = subcomponent1
    >>> input1.quantity = 2
    >>> input2 = BOMInput()
    >>> subbom.inputs.append(input2)
    >>> input2.product = subcomponent2
    >>> input2.quantity = 2
    >>> output = BOMOutput()
    >>> subbom.outputs.append(output)
    >>> output.product = component1
    >>> output.quantity = 1
    >>> subbom.save()

    >>> component1.boms.append(ProductBom(bom=subbom))
    >>> component1.save()

Get stock locations::

    >>> Location = Model.get('stock.location')
    >>> warehouse_loc, = Location.find([('code', '=', 'WH')])
    >>> supplier_loc, = Location.find([('code', '=', 'SUP')])
    >>> customer_loc, = Location.find([('code', '=', 'CUS')])
    >>> output_loc, = Location.find([('code', '=', 'OUT')])
    >>> storage_loc, = Location.find([('code', '=', 'STO')])

Create Order Point::

    >>> OrderPoint = Model.get('stock.order_point')
    >>> order_point = OrderPoint()
    >>> order_point.product = product
    >>> order_point.warehouse_location = warehouse_loc
    >>> order_point.type = 'production'
    >>> order_point.min_quantity = 1
    >>> order_point.max_quantity = 15
    >>> order_point.save()

Create Production Requests::

    >>> create_production_requests = Wizard('production.create_request')
    >>> create_production_requests.execute('create_')

Create Stock Reservations::

    >>> Production = Model.get('production')
    >>> create_reservations = Wizard('stock.create_reservations')
    >>> create_reservations.execute('create_')
    >>> productions = Production.find([])
    >>> prod1, prod2, prod3, prod4, prod5 = productions
    >>> len(prod1.parents)
    1
    >>> prod1.parents == [prod1]
    True
    >>> len(prod1.children)
    3
    >>> prod1.children == [prod1, prod2, prod3]
    True
    >>> len(prod2.parents)
    1
    >>> prod2.parents == [prod1]
    True
    >>> len(prod3.parents)
    1
    >>> prod3.parents == [prod1]
    True
    >>> len(prod2.children)
    2
    >>> prod2.children == [prod4, prod5]
    True
    >>> len(prod3.children)
    0
    >>> len(prod4.parents)
    1
    >>> prod4.parents == [prod2]
    True
    >>> len(prod4.children)
    0
    >>> len(prod5.parents)
    1
    >>> prod5.parents == [prod2]
    True
    >>> len(prod5.children)
    0
