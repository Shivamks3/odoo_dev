# -*- coding: utf-8 -*-


from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    company_type = fields.Selection(selection_add=[('om', 'Odoo Mates'), ('odoodev', 'Odoo Dev')])


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'
   # Item_name = fields.Char(String = 'Item Name')
    @api.multi
    def action_confirm(self):
        print("Shivam Singh")
        res = super(SaleOrderInherit, self).action_confirm()
        return res

    patient_name = fields.Char(string='Patient Name')
    is_patient = fields.Boolean(string='Is Patient')

class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _description = 'Patient Record'

    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'patient_name'

    patient_name = fields.Char(String='Name', required=True, track_visibility=True)
    patient_age = fields.Integer('Age', track_visibility=True, group_operator=False)
    patient_age2 = fields.Float(string="Age2")
    notes = fields.Text(String="Notes", track_visibility=True)
    image = fields.Binary(string="Image", track_visibility=True)
    name = fields.Char(String="Test", track_visibility=True)
    appointment_count = fields.Integer(string='Appointment', compute='get_appointment_count')
    active = fields.Boolean("Active", default = True )
    doctor_id = fields.Many2one('hospital.doctor', string='Doctor')
    user_id = fields.Many2one('res.users', string="PRO")
    email_id = fields.Char(string="Email")
    patient_name_upper = fields.Char(compute='_compute_upper_name', inverse='_inverse_upper_name')


    def action_patients(self):
        print("Shivam Singh..............")
        return {
            'name': _('Patients Server Action'),
            'domain': [],
            'view_type': 'form',
            'res_model': 'hospital.patient',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }

    # Sending Email in Button Click
    def action_send_card(self):
        # sending the patient report to patient via email
        template_id = self.env.ref('shivam_hospital.patient_card_email_template').id
        template = self.env['mail.template'].browse(template_id)
        template.send_mail(self.id, force_send=True)

    # How to Write Onchange Functions
    @api.onchange('doctor_id')
    def set_doctor_gender(self):
        for rec in self:
            if rec.doctor_id:
                rec.doctor_gender = rec.doctor_id.gender

    @api.model
    def test_cron_job(self):
        print("Abcd")  # print will get printed in the log of pycharm
        # code accordingly to execute the cron


    def name_get(self):
        # name get function for the model executes automatically
        res = []
        for rec in self:
            res.append((rec.id, '%s - %s' % (rec.name_seq, rec.patient_name)))
        return res


    @api.constrains('patient_age')
    def check_age(self):
        for rec in self:
            if rec.patient_age < 5:
                raise ValidationError(_('age Must be Greater Than 5..!'))


    @api.depends('patient_age')
    def set_age_group(self):
        for rec in self:
            if rec.patient_age:
                if rec.patient_age < 18:
                    rec.age_group = 'minor'
                else:
                    rec.age_group = 'major'

    gender = fields.Selection([
        ('male', 'Male'),
        ('fe_male', 'Female'),
    ], default='male', string="Gender", track_visibility=True)

    doctor_gender = fields.Selection([
        ('male', 'Male'),
        ('fe_male', 'Female'),
    ], string="Doctor Gender")

    age_group = fields.Selection([
        ('minor', 'Minor'),
        ('major', 'Major'),
    ], string="age Group", compute='set_age_group', store=True)

    # name_seq= fields.Ch
    #
    #
    #
    # ar(string = 'Order reference', required = True, copy = False, readonly = True, index =True, default = lambda self: _('New'))

    name_seq = fields.Char(string='patient ID', required=True, copy=False, readonly=True,
                           index=True, default=lambda self: _('New'))

    @api.multi
    def open_patient_appointments(self):
        return {
            'name': _('Appointments'),
            'domain': [('patient_id', '=', self.id)],
            'view_type': 'form',
            'res_model': 'hospital.appointment',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }

    def get_appointment_count(self):
        count = self.env['hospital.appointment'].search_count([('patient_id', '=', self.id)])
        self.appointment_count = count

    def _inverse_upper_name(self):
        for rec in self:
            rec.patient_name = rec.patient_name_upper.lower() if rec.patient_name_upper else False

    @api.depends('patient_name')
    def _compute_upper_name(self):
        for rec in self:
            rec.patient_name_upper = rec.patient_name.upper() if rec.patient_name else False


    # Print PDF Report From Button Click in Form
    @api.multi
    def print_report(self):
        return self.env.ref('shivam_hospital.report_patient_card').report_action(self)


    @api.model
    def create(self, vals):
        if vals.get('name_seq', _('New')) == _('New'):
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('hospital.patient.sequence') or _('New')

        result = super(HospitalPatient, self).create(vals)
        return result


