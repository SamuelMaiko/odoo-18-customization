{
    'name': 'National ID Application',
    'version': '1.0',
    'category': 'Website',
    'summary': 'Online application for national ID with approval workflow',
    'author': 'Samuel Maiko',
    'depends': ['base', 'website'], # NOTE - why base, others don't have it
    'data': [
        # 'security/security.xml', #NOTE - others don't have it
        # 'views/templates.xml',
        'security/groups.xml',
        'views/apply_form_template.xml',
        'views/thank_you_template.xml',
        'views/backend_views.xml',
        'security/record_rules.xml',
        'security/ir.model.access.csv',
    ],
    'assets': {
            'web.assets_frontend': [

            ],
        },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}