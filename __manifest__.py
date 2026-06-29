# -*- coding: utf-8 -*-
#############################################################################
#
#    Techvaria Solutions Pvt. Ltd.
#
#    Copyright (C) 2026-Techvaria Solutions(<https://techvaria.com>)
#    Author: Techvaria Solutions Pvt. Ltd.(info@techvaria.com)
#
#    You can modify it under the terms of the GNU AFFERO
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU AFFERO GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
#    You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
#    (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################

{
    'name': 'Garage Management System',
    'version': '18.0.1.0.0',
    'category': 'Industries',
    'summary': 'Complete Garage Management System for vehicle service and workshop operations',
    'description': """
        This module provides a complete Garage Management System for automobile workshops.

    """,
    'author': 'Techvaria',
    'company': 'Techvaria',
    'maintainer': 'Techvaria',
    'support': 'support@techvaria.com',
    'website': 'https://techvaria.com',
    'depends': [
        'sale_management',
        'purchase',
        'stock',
        'contacts',
        'hr',
        'account'
    ],
    'data': [
            'data/sequences.xml',
            'data/mail_template.xml',
            'data/corn_package_state.xml',
            'wizard/diagnosis_wizard_view.xml',
            'security/res_groups.xml',
            'security/ir.model.access.csv',
            'views/product_template_views.xml',
            'views/vehicle_workshop_view.xml',
            'views/service_request_view.xml',
            'views/service_type_view.xml',
            'views/job_card_view.xml',
            'views/service_category_view.xml',
            'views/service_checklist_view.xml',
            'views/service_packages_view.xml',
            'views/job_timesheet_view.xml',
            'views/work_order_view.xml',
            'views/check_list_line_view.xml',
            'views/job_card_checklist_line_view.xml',
            'views/diagnosis_view.xml',
            'views/package_service_line_view.xml',
            'views/job_card_service_charge_line_view.xml',
            'views/job_card_vehicle_spare_parts_view.xml',
            'views/job_card_timesheet_line_view.xml',
            'views/sale_order_view.xml',
            'views/purchase_order_view.xml',
            'views/job_images_view.xml',
            'views/garage_vehicle_make_view.xml',
            'views/garage_vehicle_model_view.xml',
            'views/vehicle_category_view.xml',
            'views/vehicle_detail_view.xml',
            'views/service_package_history_view.xml',
            'views/res_partner_view.xml',
            'views/menu_view.xml',
    ],
    'images': [
        'static/description/screen.png',
    ],
    'license': 'OPL-1',
    'installable': True,
    'auto_install': False,
    'application': True,
}
