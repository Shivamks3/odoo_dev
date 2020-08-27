from odoo import api, models, _


# How To Call A Python Function While Printing PDF Report in Odoo

class PatientCardReport(models.AbstractModel):
    _name = 'report.shivam_hospital.report_patient'
    _description = 'Patient card Report'

    @api.model
    def get_report_values(self, docids, data=None):
        docs = self.env['hospital.patient'].browse(docids[0])
        appointments = self.env['hospital.appointment'].search([('patient_id', '=', docids[0])])
        appointment_list = []
        for app in appointments:
            vals = {
                'name': app.name,
                'notes': app.notes,
                'appointment_date': app.appointment_date
            }
            appointment_list.append(vals)
        return {
            'doc_model': 'hospital.patient',
            'docs': docs,
            'appointment_list': appointment_list,
        }