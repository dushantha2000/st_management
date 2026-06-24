from odoo import models, fields, api, _
from datetime import date, datetime, timedelta
from odoo.exceptions import ValidationError


class StudentStudent(models.Model):
    _name = 'student.student'
    _description = 'Student Records'

    # log note handling
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # --------------------------------------------------------------------------------------

    # db fields
    name = fields.Char(
        string='Name',
        required=True,
        tracking=True
    )

    age = fields.Integer(
        string='Age',
        compute='_compute_nic_checker',
        store=True,
        tracking=True)

    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ],
        string='Gender',
        default='male',
        tracking=True
    )

    address = fields.Char(
        string='Address',
        required=True,
        tracking=True
    )

    phone_number = fields.Char(
        string='Phone Number',
        required=True,
        tracking=True,
        default='07++++++++'
    )

    nationality = fields.Selection([
        ('srilankan', 'Srilankan'),
        ('other', 'Other')
    ],
        string='Nationality',
        default='srilankan',
        tracking=True
    )

    dob = fields.Date(
        string='Date of Birth',
        compute='_compute_nic_checker',
        store=True,
        tracking=True
    )

    registration_id = fields.Char(
        string='Student ID',
        required=True,
        copy=False,
        readonly=True,
        index=True,
        default=lambda self: _('New'),
        tracking=True
    )

    # NIC number
    nic_number = fields.Char(
        string='NIC Number',
        required=True,
        tracking=True
    )

    _sql_constraints = [(
        'nic_number_unique',
        'unique(nic_number)',
        'The NIC must be unique!'
    )]

    # ---------------------------------------------------------------------------------------

    # Relational fields
    course_ids = fields.Many2many(
        'course.course',
        'student_course_rel',
        'student_id',
        'course_id',
        string='Enrolled Courses',
        required=True
    )

    fee_ids = fields.One2many(
        'student.fees',
        'student_id',
        string='Fees History'
    )

    # _sql_constraints = [
    #     ('unique_nic_number', 'unique(nic_number)', 'Student NIC Number already registered.')
    # ]

    # ----------------------------------------------------------------------------------------------

    # NIC format verification
    @api.constrains('nic_number')
    def _check_nic_number(self):
        for record in self:

            if not record.nic_number:
                continue

            # raise ValidationError('error')

            nic = record.nic_number.strip()
            is_old = len(nic) == 10 and nic[:9].isdigit() and nic[-1].upper() in ['V', 'X']
            is_new = len(nic) == 12 and nic.isdigit()

            if not (is_old or is_new):
                raise ValidationError(
                    _(" Invalid NIC Number format. Please enter a valid Sri Lankan NIC ")
                )

    # ------------------------------------------------------------------------------------------

    @api.depends('nic_number')
    def _compute_nic_checker(self):
        for record in self:

            # Default values
            record.dob = False
            record.age = 0

            if not record.nic_number:
                continue

            nic = str(record.nic_number).strip()
            year = None
            days = 0

            try:
                # Extract Year and Days based on NIC format
                if len(nic) == 10 and nic[:9].isdigit() and nic[-1].upper() in ['V', 'X']:

                    # Old NIC Format

                    year = int("19" + nic[:2])
                    days = int(nic[2:5])

                elif len(nic) == 12 and nic.isdigit():

                    # New NIC Format

                    year = int(nic[:4])
                    days = int(nic[4:7])
                else:

                    # Invalid format
                    continue

                if days > 500:
                    days -= 500
                    record.gender = 'female'
                else:
                    record.gender = 'male'

                # Cal Birthday

                base_date = datetime(year - 1, 12, 31)
                dob_date = base_date + timedelta(days=days)
                record.dob = dob_date.date()

                # Cal Age
                today = date.today()
                if record.dob:
                    record.age = today.year - record.dob.year - (
                            (today.month, today.day) < (record.dob.month, record.dob.day)
                    )

            except Exception:
                record.dob = False
                record.age = 0

    # --------------------------------------------------------------------------------------------

    # create ID auto

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('registration_id', _('New')) == _('New'):
                vals['registration_id'] = self.env['ir.sequence'].next_by_code('student.student') or _('New')
        return super(StudentStudent, self).create(vals_list)

    # -------------------------------------------------------

    # phone number verification
    @api.constrains('phone_number')
    def _check_phone_number(self):
        for record in self:

            # empty fields handling
            if not record.phone_number:
                continue

            # remove extra spaces
            phone = record.phone_number.strip()

            if not phone.isdigit():
                raise ValidationError(
                    "Invalid Format: Phone number must contain only numbers (0-9). Please remove spaces, hyphens, or letters."
                )

            if len(phone) != 10:
                raise ValidationError(
                    f"Invalid Length: Phone number must be exactly 10 digits long."
                )

    # -------------------------------------------------------------------------------------------------

    # NIC format verification
    @api.constrains('nic_number')
    def _check_nic_number(self):
        for record in self:

            if not record.nic_number:
                continue

            nic = record.nic_number.strip()
            is_old = len(nic) == 10 and nic[:9].isdigit() and nic[-1].upper() in ['V', 'X']
            is_new = len(nic) == 12 and nic.isdigit()

            if not (is_old or is_new):
                raise ValidationError(
                    _("Invalid NIC Number format. Please enter a valid Sri Lankan NIC (e.g., 99001001V or 199900100001).")
                )


