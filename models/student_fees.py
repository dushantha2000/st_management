from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class StudentFees(models.Model):
    _name = 'student.fees'
    _description = 'Student Fees Management'

    # log note handling
    _inherit = ['mail.thread', 'mail.activity.mixin']


    _order = 'date desc'


    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default=lambda self: _('New'),tracking=True)

    student_id = fields.Many2one('student.student', string='Student', required=True, tracking=True)

    student_course_ids = fields.Many2many('course.course', related='student_id.course_ids', string="Student's Enrolled Courses",tracking=True)

    course_id = fields.Many2one('course.course', string='Course', required=True, tracking=True)

    nic_number = fields.Char(string='NIC Number', required=True, tracking=True)

    amount_total = fields.Float(string='Total Amount', compute='_compute_amount_total', store=True, readonly=True,tracking=True)

    amount_paid = fields.Float(string='Amount Paid', required=True, tracking=True)

    amount_balance = fields.Float(string='Balance', compute='_compute_balance', store=True,tracking=True)

    date = fields.Date(string='Payment Date', default=fields.Date.context_today, tracking=True)
    payment_method = fields.Selection([
        ('cash', 'Cash'),
        ('bank', 'Bank Transfer'),
        ('card', 'Credit/Debit Card')
    ], string='Payment Method', default='cash', tracking=True)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('cancel', 'Payment Close')
    ], string='Status', default='draft', tracking=True)






    @api.depends('amount_total', 'amount_paid')
    def _compute_balance(self):
        for record in self:
            record.amount_balance = record.amount_total - record.amount_paid
            if record.state != 'draft':
                if record.amount_balance == 0:
                    record.state = 'paid'
                elif record.amount_balance > 0:
                    record.state = 'pending'
                else:
                    record.state = 'cancel'







    @api.depends('student_id', 'course_id', 'state')
    def _compute_amount_total(self):
        for record in self:
            if record.student_id and record.course_id:
                full_course_fee = record.course_id.standard_price
                past_payments = self.env['student.fees'].search([
                    ('student_id', '=', record.student_id.id),
                    ('course_id', '=', record.course_id.id),

                    # ('state', '=', 'draft'),

                    ('id', '!=', record.id or 0)
                ])
                total_past_paid = sum(past_payments.mapped('amount_paid'))
                record.amount_total = full_course_fee - total_past_paid


            else:
                record.amount_total = 0.0




    @api.constrains('amount_paid', 'amount_total')
    def _check_payment_amount(self):
        for record in self:
            if record.amount_paid > record.amount_total:
                raise ValidationError(
                    _("Amount Paid cannot exceed Total Amount (%s).")
                    % record.amount_total
                )

            if record.amount_total == 0 :
                raise ValidationError(
                    _("This course fee is already fully paid. You cannot process a payment of %s.")
                    % record.amount_paid

                )







    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('student.fees') or _('New')
        return super().create(vals_list)










    def action_confirm(self):
        for record in self:
            if record.amount_balance == 0:
                record.state = 'paid'
            else:
                record.state = 'pending'



    def action_cancel(self):
        for record in self:
            record.state = 'cancel'
