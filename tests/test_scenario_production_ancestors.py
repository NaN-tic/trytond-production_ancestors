import datetime
import unittest
from decimal import Decimal

from dateutil.relativedelta import relativedelta
from proteus import Model
from trytond.modules.company.tests.tools import create_company
from trytond.tests.test_tryton import drop_db
from trytond.tests.tools import activate_modules


class Test(unittest.TestCase):

    def setUp(self):
        drop_db()
        super().setUp()

    def tearDown(self):
        drop_db()
        super().tearDown()

    def test(self):

        today = datetime.date.today()
        today - relativedelta(days=1)

        # Install production Module
        activate_modules(['production_ancestors', 'stock_supply_production'])

        # Create company
        _ = create_company()

        # Create product
        ProductUom = Model.get('product.uom')
        unit, = ProductUom.find([('name', '=', 'Unit')])
        ProductTemplate = Model.get('product.template')
        Product = Model.get('product.product')
        product = Product()
        template = ProductTemplate()
        template.name = 'product'
        template.default_uom = unit
        template.producible = True
        template.type = 'goods'
        template.list_price = Decimal(30)
        template.save()
        product.template = template
        product.cost_price = Decimal(20)
        product.save()

        # Create Components
        component1 = Product()
        template1 = ProductTemplate()
        template1.name = 'component 1'
        template1.default_uom = unit
        template1.type = 'goods'
        template1.list_price = Decimal(5)
        template1.producible = True
        template1.save()
        component1.template = template1
        component1.cost_price = Decimal(1)
        component1.save()
        component2 = Product()
        template2 = ProductTemplate()
        template2.name = 'component 2'
        template2.default_uom = unit
        template2.type = 'goods'
        template2.list_price = Decimal(5)
        template2.save()
        component2.template = template2
        component2.cost_price = Decimal(1)
        component2.save()

        # Create Subcomponents
        subcomponent1 = Product()
        template3 = ProductTemplate()
        template3.name = 'subcomponent 1'
        template3.default_uom = unit
        template3.type = 'goods'
        template3.list_price = Decimal(5)
        template3.save()
        subcomponent1.template = template3
        subcomponent1.cost_price = Decimal(1)
        subcomponent1.save()
        subcomponent2 = Product()
        template4 = ProductTemplate()
        template4.name = 'subcomponent 2'
        template4.default_uom = unit
        template4.type = 'goods'
        template4.list_price = Decimal(5)
        template4.save()
        subcomponent2.template = template1
        subcomponent2.cost_price = Decimal(1)
        subcomponent2.save()

        # Create Bill of Material
        BOM = Model.get('production.bom')
        BOMInput = Model.get('production.bom.input')
        BOMOutput = Model.get('production.bom.output')
        bom = BOM(name='product')
        input1 = BOMInput()
        bom.inputs.append(input1)
        input1.product = component1
        input1.quantity = 2
        input2 = BOMInput()
        bom.inputs.append(input2)
        input2.product = component2
        input2.quantity = 2
        output = BOMOutput()
        bom.outputs.append(output)
        output.product = product
        output.quantity = 1
        bom.save()
        ProductBom = Model.get('product.product-production.bom')
        product.boms.append(ProductBom(bom=bom))
        product.save()

        # Create sub Bill of Material
        subbom = BOM(name='component 1')
        input1 = BOMInput()
        subbom.inputs.append(input1)
        input1.product = subcomponent1
        input1.quantity = 2
        input2 = BOMInput()
        subbom.inputs.append(input2)
        input2.product = subcomponent2
        input2.quantity = 2
        output = BOMOutput()
        subbom.outputs.append(output)
        output.product = component1
        output.quantity = 1
        subbom.save()
        component1.boms.append(ProductBom(bom=subbom))
        component1.save()

        # Get stock locations
        Location = Model.get('stock.location')
        warehouse_loc, = Location.find([('code', '=', 'WH')])
        supplier_loc, = Location.find([('code', '=', 'SUP')])
        customer_loc, = Location.find([('code', '=', 'CUS')])
        output_loc, = Location.find([('code', '=', 'OUT')])
        storage_loc, = Location.find([('code', '=', 'STO')])

        # Create Order Point
        OrderPoint = Model.get('stock.order_point')
        order_point = OrderPoint()
        order_point.product = product
        order_point.warehouse_location = warehouse_loc
        order_point.type = 'production'
        order_point.target_quantity = 15
        order_point.min_quantity = 1
        order_point.max_quantity = 15
        order_point.save()
