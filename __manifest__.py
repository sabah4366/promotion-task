{
    'name': "Promotion And Increment",
    'version': '17.0.1.0.0',
    'summary': """promotion and increment""",
    'sequence':-1,
    'description': """
    """,
    'author': "My Company",
    'company': 'My Company',
    'maintainer': 'My Company',
    'depends': ['base','hr'],
    'data': [
        'security/ir.model.access.csv',
        'security/security_groups.xml',
        'views/hr_department.xml',
    ],

    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,
}
