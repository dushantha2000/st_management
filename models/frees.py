
from odoo import models, fields

class Frees(course.fees):
    _name = 'course.fees'
    _description = 'courses Frees'


    # log note handling
    _inherit = ['mail.thread', 'mail.activity.mixin']



    course_ids = fields.Many2one('course.course', string=' Courses', required=True)

    fees = fields.float( string=' Courses', required=True)

    student_id =fields.Many2one('course.course', string=' Courses', required=True)

    Last_price = fields.Float(string=' Last Price', required=True)

    state = fields.Selection([('paid', 'paid'), ('unpaid', 'unpaid'),
                              ('pending', 'pending'),('Cancelled', 'Cancelled')], string='Status', default='pending')

    registered_date = fields.date(string='registered date' ,required=True)

    paided_date = fields.date(string='paid date' ,required=True ,default='')

    fee_pay_last_date = fields.Float(string=' Fee Pay Last Date', required=True)

  
    Action = fields.Selection([('block', 'block'), ('pending', 'pending')])

    payment_method = fields.Selection([
        ('cash', 'Cash'),
        ('bank', 'Bank Transfer'),
        ('card', 'Credit/Debit Card'),
        ('-', '-')
    ], string='Payment Method')


































