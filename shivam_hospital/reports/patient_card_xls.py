from odoo import models



class PatientCardXLS(models.AbstractModel):
    
    #_wrapped_report_class = patient_card_xls
    _name = 'report.shivam_hospital.report_patient_xls'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        format1 = workbook.add_format({'font_size': 14, 'align': 'vcenter', 'bold': True})
        format2 = workbook.add_format({'font_size': 10, 'align': 'vcenter', })
        sheet = workbook.add_worksheet('Patient Card')

        sheet.right_to_left()

        sheet.set_column(3, 3, 50)
        sheet.set_column(2, 2, 30)
        sheet.write(2, 2, 'Name', format1)
        sheet.write(2, 3, lines.patient_name, format2)
        sheet.write(3, 2, 'Age', format1)
        sheet.write(3, 3, lines.patient_age, format2)