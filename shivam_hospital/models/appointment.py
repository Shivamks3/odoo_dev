# -*- coding: utf-8 -*-

import pytz
from odoo import models, fields, api,  _
from datetime import datetime


class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _description = 'Appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "appointment_date desc"


    def test_recordset(self):
        for rec in self:
            print("Odoo ORM: Record Set Operation")
            partners = self.env['res.partner'].search([])
            print("Mapped partners...", partners.mapped('email'))
            print(" Sorted partners...", partners.sorted(lambda o: o.write_date, reverse=True))
            print(" Filtered partners...", partners.filtered(lambda o: not o.customer))


    @api.model
    def create(self, vals):
        # overriding the create method to add the sequence
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hospital.appointment') or _('New')
        result = super(HospitalAppointment, self).create(vals)
        return result


    def action_notify(self):
        for rec in self:
            rec.doctor_id.user_id.notify_warning(message='Appointment is Confirmed')


    def action_confirm(self):
        for rec in self:
            rec.state = 'confirm'
            return {
                'effect': {
                    'fadeout': 'slow',
                    'message': 'Appointment Confirmed... Thanks You',
                    'type': 'rainbow_man',
                }
            }

    def action_done(self):
        for rec in self:
            rec.state = 'draft'


    def delete_lines(self):
        for rec in self:
            dt = datetime.strptime(rec.appointment_date, '%Y-%m-%d %H:%M:%S')
            print('Date in UTC1:', dt)
            time_zone = pytz.timezone(self.env.context.get('tz') or self.env.user.tz)
            date_today = pytz.utc.localize(dt).astimezone(time_zone)
            print('Today Date', date_today)
            #user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz)
           # user_tz = pytz.timezone(self.env.context.get('tz')) if self.env.context.get('tz') else self.env.user.tz
            #time_in_timezone = pytz.utc.localize(rec.appointment_datetime).astimezone(user_tz)

            # print("Time in UTC -->", rec.appointment_datetime)
            # print("Time in Users Timezone -->", time_in_timezone)
            rec.appointment_lines = [(5, 0, 0)]
           # 'patient_id': vals['patient_id'] if vals.get('patient_id') else False,



    # Give Domain For A field dynamically in Onchange
    # How To Give Domain For A Field Based On Another Field
    @api.onchange('partner_id')
    def onchange_partner_id(self):
        for rec in self:
            return {'domain': {'order_id': [('partner_id', '=', rec.partner_id.id)]}}


    @api.model
    @api.model
    def default_get(self, fields):
        res = super(HospitalAppointment, self).default_get(fields)
        appointment_lines = []
        product_rec = self.env['product.product'].search([])
        for pro in product_rec:
            line = (0, 0, {
                'product_id': pro.id,
                'product_qty': 1,
            })
            appointment_lines.append(line)
        res.update({
            'appointment_lines': appointment_lines,
            'patient_id': 1,
            'notes': 'Like and Subscribe our channel To Get Notified'
        })
        return res


    @api.multi
    def write(self, vals):
        # overriding the write method of appointment model
        res = super(HospitalAppointment, self).write(vals)
        print("Test write function")
        # do as per the need
        return res


    name = fields.Char(string='Appointment ID', required=True, copy=False, readonly=True,
                       index=True, default=lambda self: _('New'))
    patient_id = fields.Many2one('hospital.patient', string='Patient', required=True)
    doctor_id = fields.Many2one('hospital.doctor', string='Doctor')
    #doctor_ids = fields.Many2many('hospital.doctor', 'hospital_patient_rel', 'appointment_id', 'doctor_id_rec',
           #                       string='Doctors')
    patient_age = fields.Integer('Age', related='patient_id.patient_age')
    notes = fields.Text(string="Registration Note")
    appointment_date = fields.Date(string='Date')
    appointment_date_end = fields.Date(string='End Date')
    appointment_datetime = fields.Datetime(string='Date Time')
    partner_id = fields.Many2one('res.partner', string="Customer")
    order_id = fields.Many2one('sale.order', string="Sale Order")
    doctor_note = fields.Text(string="Note", track_visibility='onchange')
    amount = fields.Float(string="Total Amount")
    #create one2many fields
    appointment_lines = fields.One2many('hospital.appointment.lines', 'appointment_id', string='Appointment Lines')
    pharmacy_note = fields.Text(string="Note", track_visibility='always')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True, default='draft')

    product_id = fields.Many2one('product.template', string="Product Template")

    @api.onchange('product_id')
    def _onchange_product_id(self):
        for rec in self:
            if rec.product_id:
                lines = [(5, 0, 0)]
                # lines = []
                print("self.product_id", self.product_id.product_variant_ids)
                for line in self.product_id.product_variant_ids:
                    val = {
                        'product_id': line.id,
                        'product_qty': 15
                    }
                    lines.append((0, 0, val))
                rec.appointment_lines = lines


class HospitalAppointmentLines(models.Model):
    _name = 'hospital.appointment.lines'
    _description = 'Appointment Lines'

    product_id = fields.Many2one('product.product', string='Medicine')
    product_qty = fields.Integer(string="Quantity")
    sequence = fields.Integer(string="Sequence")
    appointment_id = fields.Many2one('hospital.appointment', string='Appointment ID')
    
    
