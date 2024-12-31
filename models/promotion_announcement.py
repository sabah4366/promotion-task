from odoo import models, fields, api


class PromotionAnnouncement(models.Model):
    _name = 'promotion.announcement'
    _description = 'Promotion Announcement'

    name = fields.Char(string="Promotion Name", required=True)
    announcement_date = fields.Date(string="Announcement Date", default=fields.Date.today)
    department_id = fields.Many2one('hr.department', string="Department", required=True)
    available_seats = fields.Integer(string="Seats per Department", default=0)
    additional_details = fields.Text(string="Additional Details")
    promotion_lines = fields.One2many('promotion.request.line', 'promotion_id', string="Promotion Requests")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('hr_review', 'HR Reviewed'),
        ('promotion_review', 'Promotion Reviewed'),
        ('ceo_approval', 'CEO Approved'),
    ], string="Status", default='draft')

    @api.model
    def create(self, vals):
        record = super(PromotionAnnouncement, self).create(vals)
        record.send_notifications()
        return record

    def action_hr_review(self):
        self.state = 'hr_review'


    def action_promotion_review(self):
        self.state = 'promotion_review'

    def action_ceo_approval(self):
        self.state = 'ceo_approval'


    def send_notifications(self):
        model_id = self.env['ir.model'].search([('model', '=', 'hr.department')], limit=1)
        if self.department_id.manager_id:
            seats = self.available_seats
            message = f"""
            Dear {self.department_id.manager_id.name},
            The promotion/increment nomination process has been opened for your department.
            Available seats: {seats}
            Details: {self.additional_details}
            Announcement Date: {self.announcement_date}
            """
            self.env['mail.activity'].create({
                'summary': 'Promotion Process Announcement',
                'note': message.strip(),
                'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,  # Default activity type
                'res_id': self.department_id.id,
                'res_model_id': model_id.id,
                'user_id': self.department_id.manager_id.id,
            })
            print('worked')


class PromotionRequestLine(models.Model):
    _name = 'promotion.request.line'
    _description = 'Promotion Request Line'

    promotion_id = fields.Many2one('promotion.announcement', string="Promotion")
    employee_id = fields.Many2one('hr.employee', string="Employee", required=True)
    current_salary = fields.Float(string="Current Salary")
    proposed_salary = fields.Float(string="Proposed Salary")
