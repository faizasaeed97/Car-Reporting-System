# -*- coding: utf-8 -*-

{
    'name': 'car_customization',
    'sequence': 1222,
    'version': '1.0',
    'depends': ['mail','base','product','account','sale'],
    'category': 'sale','crm'
    'summary': 'Handle lunch orders of your employees',
    'description': """
The base module to manage lunch.
================================
Cost sheet from CRM, Generate Quotation
    """,
    'data': [
        'views/view.xml',
        'security/rec_rules.xml',
        'security/rec_rules2.xml',
        'views/cron.xml',
        'views/reportview.xml' ,
        'views/wizard.xml' ,
        'views/carreport.xml' ,
        'views/carreporttemplate.xml' ,
        'views/inheritreport.xml' ,
        'views/inheritrepair.xml' ,
        'views/reporttemplate.xml' ,
        'security/ir.model.access.csv',

    ],
    'installable': True,
    'application': True,
}
