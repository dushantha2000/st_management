from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class StudentFees(models.Model):

    _name = 'student.fees'
    _description = 'Student Fees Management'

    # log note handling
    _inherit = ['mail.thread', 'mail.activity.mixin']


    _order = 'date desc'

    # --------------------------------------------------------------------------------------

    #db relations

    student_course_ids = fields.Many2many(
        'course.course',
        related='student_id.course_ids',
        string="Student's Enrolled Courses",
        tracking=True
    )

    course_id = fields.Many2one(
        'course.course',
        string='Course',
        required=True,
        tracking=True
    )

    student_id = fields.Many2one(
        'student.student',
        string='Student',
        required=True,
        tracking=True)

    # ----------------------------------------------------------------------------------------


    name = fields.Char(
        string='Reference',
        required=True, copy=False,
        readonly=True,
        default=lambda self: _('New'),
        tracking=True
    )


    amount_total = fields.Float(
        string='Total Amount',
        compute='_compute_amount_total',
        store=True,
        readonly=True,
        tracking=True
    )

    amount_paid = fields.Float(
        string='Amount Paid',
        required=True,
        tracking=True
    )

    amount_balance = fields.Float(
        string='Balance',
        compute='_compute_balance',
        store=True,
        tracking=True
    )

    date = fields.Date(
        string='Payment Date',
        default=fields.Date.context_today,
        tracking=True
    )


    payment_method = fields.Selection([
        ('cash', 'Cash'),
        ('bank', 'Bank Transfer'),
        ('card', 'Credit/Debit Card')
    ], string='Payment Method',
        default='cash',
        tracking=True
    )

    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('cancel', 'Payment Close')
    ], string='Status', default='draft', tracking=True)


    # --------------------------------------------------------------------------------------------------------

    # link create invoice

    move_id = fields.Many2one(
        'account.move',
        string='Invoice',
        readonly=True,
        copy=False
    )
    invoice_state = fields.Selection(
        related='move_id.state',
        string='Invoice Status',
        store=True
    )

    # partner_id = fields.Many2one(
    #     'res.partner',
    #     string='Accounting Contact',
    #     ondelete='restrict',
    #     tracking=True
    # )

    # --------------------------------------------------------------------------------------------------

    # create invoice
    def action_create_invoice(self):

        self.ensure_one()


        # Income account
        account = self.env['account.account'].search([
            ('account_type', '=', 'income')
        ], limit=1)


        if not account:
            raise UserError(_("No Income Account found."))



        # Get or create partner from student name
        partner = self.env['res.partner'].search([
            ('name', '=', self.student_id.name)
        ], limit=1)


        if not partner:
            partner = self.env['res.partner'].create({
                'name': self.student_id.name,
            })

        # Build invoice
        invoice_vals = {
            #must need pass  "move_type" in coming or out going
            'move_type': 'out_invoice',

            #must need pass  "partner_id" that is student_id
            'partner_id': partner.id,

            'invoice_date': fields.Date.today(),

            'ref': self.name,

            #Internal Note
            'narration': _(
                'Course Fee Payment\nStudent: %s\nCourse: %s'
            ) % (self.student_id.name, self.course_id.name),


            'invoice_line_ids': [(0, 0, {
                'name': _('Course Fee: %s') % self.course_id.name,
                # 'quantity': 1.0,
                'price_unit': self.amount_paid,
                'account_id': account.id,
            })],
        }

        # Create and post
        invoice = self.env['account.move'].create(invoice_vals)
        invoice.action_post()



        # Link and update state
        self.move_id = invoice.id
        self.state = 'pending'

        # Open invoice
        return {
            'type': 'ir.actions.act_window',
            'name': _('Invoice'),
            'res_model': 'account.move',
            'res_id': invoice.id,
            'view_mode': 'form',
            'target': 'current',
        }

    # -----------------------------------------------------------------------------------------------------



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
