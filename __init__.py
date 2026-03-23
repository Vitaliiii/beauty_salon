from . import models
from . import wizard
from . import report

import odoo
if odoo.tools.config['test_enable']:
    from . import tests