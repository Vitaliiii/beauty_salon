from . import models
from . import wizard

import odoo
if odoo.tools.config['test_enable']:
    from . import tests