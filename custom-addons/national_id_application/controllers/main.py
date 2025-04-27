from odoo import http
from odoo.http import request
import base64


class NationalIDWebsite(http.Controller):
    @http.route(['/national-id/apply'], type='http', auth='public', website=True)
    def apply_form(self, **kwargs):
        return request.render('national_id_application.apply_form_template')

    @http.route(['/national-id/submit'], type='http', auth='public', website=True, methods=['POST'])
    def submit_application(self, **post):
        picture_file = post.get('picture')
        lc_letter_file = post.get('lc_letter')

        picture_data = False
        lc_letter_data = False

        if picture_file:
            picture_data = base64.b64encode(picture_file.read())

        if lc_letter_file:
            lc_letter_data = base64.b64encode(lc_letter_file.read())

        request.env['national.id.application'].sudo().create({
            'name': post.get('name'),
            'date_of_birth': post.get('date_of_birth'),
            'place_of_birth': post.get('place_of_birth'),
            'email': post.get('email'),
            'phone': post.get('phone'),
            'picture': picture_data,
            'lc_reference_letter': lc_letter_data,
        })
        return request.render('national_id_application.thank_you_template')