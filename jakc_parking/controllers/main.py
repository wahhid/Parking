import base64
import mimetypes

import openerp.addons.web.http as oeweb
from openerp.addons.web.controllers.main import content_disposition


#----------------------------------------------------------
# Controller
#----------------------------------------------------------
class ParkingController(oeweb.Controller):
    _cp_path = '/parking'

    @oeweb.httprequest
    def download_attachment(self, req, model, id, method, attachment_id, **kw):
        Model = req.session.model(model)
        res = getattr(Model, method)(int(id), int(attachment_id))
        if res:
            filecontent = base64.b64decode(res.get('base64'))
            filename = res.get('filename')
            content_type = mimetypes.guess_type(filename)
            if filecontent and filename:
                return req.make_response(filecontent,
                    headers=[('Content-Type', content_type[0] or 'application/octet-stream'),
                            ('Content-Disposition', content_disposition(filename, req))])
        return req.not_found()
    
    @oeweb.httprequest
    def imageview(self, req, model, attachment_id, **kw):
        Model = req.session.model(model)
        headers = [('Content-Type', 'image/jpg')]                    
        res = Model.read([id], ['datas'], req.context)[0]        
        if res:
            image_data = base64.b64decode(res.get('datas'))            
            return req.make_response(image_data,headers)
        return req.not_found()
    