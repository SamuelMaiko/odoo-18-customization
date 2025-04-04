{
    'name': 'Purchase Request',
    'version': '1.0',
    'category': 'Purchases',
    'summary': 'Employee Purchase Requests for Procurement',
    'depends': ['purchase', 'hr'],
    'data': [
        "security/ir.model.access.csv",
        "views/purchase_request_views.xml",
        # 'security/purchase_request_security.xml',
        # 'security/ir.model.access.csv',
        # 'views/purchase_request_views.xml',
        # 'views/purchase_request_line_views.xml',
        # 'data/mail_templates.xml',
    ],
    'installable': True,
    'application': True,
}