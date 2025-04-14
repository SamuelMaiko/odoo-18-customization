{
    'name': 'Purchase Request',
    'version': '1.0',
    'category': 'Purchases',
    'summary': 'Employee Purchase Requests for Procurement',
    'author': 'Samuel Maiko',
    'depends': ['base','purchase', 'hr'],
    'data': [
        "data/hr_department_data.xml",
        'data/purchase_request_sequence.xml',
        "views/purchase_request_views.xml",
        "security/group_procurement_approver.xml",
        "security/ir.model.access.csv",
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}