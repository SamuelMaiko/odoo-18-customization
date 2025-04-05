{
    'name': 'Multi Vendor RFQ',
    'version': '1.0',
    'category': 'Purchases',
    'summary': 'Enable assigning a single RFQ to multiple vendors',
    'author': 'Samuel Maiko',
    'depends': ['purchase','mail'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/purchase_order_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}