import json
import logging
import werkzeug
import werkzeug.utils
from datetime import datetime
from math import ceil

from openerp import SUPERUSER_ID
from openerp.addons.web import http
from openerp.http import request
from openerp.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT as DTF, ustr


_logger = logging.getLogger(__name__)


class WebsiteParking(http.Controller):

    @http.route('/parking/trans/index/', type='http', auth='public', website=True)
    def parking_trans_index(self, platnumber=None):
        data = {}
        return request.website.render('parking.parking_transaction_index', data)
