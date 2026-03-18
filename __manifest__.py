{
    'name': 'Beauty Salon Management',
    'version': '19.0.1.0.0',
    'category': 'Services',
    'summary': 'A comprehensive management system for beauty salons, barbershops, and SPAs',
    'description': """
Beauty Salon Management System
==============================
This module provides a complete set of tools to automate beauty salon operations:

Key Features:
-------------
* **Appointments:** Convenient calendar for booking time slots and avoiding schedule overlaps.
* **Client Base:** Maintains visit history, contact information, and client photos.
* **Master Catalog:** Management of specialists, their contacts, and individual bonus percentages.
* **Service Pricelist:** Management of services with fixed prices and durations.
* **Finance & Reports:** Automatic calculation of masters' payroll (bonuses) and PDF report generation.
* **Automation (CRON):** Automated reminder system for 'forgotten' clients (no visits for over 30 days).
* **Analytics:** Built-in pivot tables and graphs for revenue analysis.
* **Security:** Multi-level access system (Masters see only their own appointments, Managers oversee everything).

This module perfectly demonstrates the use of key Odoo 19 framework technologies.
    """,
    'author': 'Vitalii',
    'website': 'https://github.com/Vitaliiii',
    'license': 'LGPL-3',
    'depends': [
        'base', 
        'mail',
        'calendar',
    ],
    'data': [
        'security/beauty_security.xml',
        'security/ir.model.access.csv',
        'views/beauty_views.xml',
        'report/bonus_report.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
    'images': ['static/description/icon.png'],
}