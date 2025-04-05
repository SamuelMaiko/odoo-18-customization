{
    'name': 'Purchase Request',
    'version': '1.0',
    'category': 'Purchases',
    'summary': 'Employee Purchase Requests for Procurement',
    'depends': ['purchase', 'hr'],
    'data': [
        "data/hr_department_data.xml",
        "views/purchase_request_views.xml",
        "security/ir.model.access.csv",
    ],
    'installable': True,
    'application': True,
}