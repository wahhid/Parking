{
    'name' : 'Parking Management System',
    'version' : '11.1.0.0',
    'author' : 'Jakc Labs',
    'category' : 'Generic Modules/Parking Management System',
    'depends' : ['base','hr', 'product', 'account', 'sale'],
    'init_xml' : [],
    'data' : [
        'security/jakc_parking_security.xml',
        'views/jakc_parking_view.xml',
        'views/jakc_parking_booth_view.xml',
        'views/jakc_parking_pricing_view.xml',
        'views/jakc_parking_menu.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}