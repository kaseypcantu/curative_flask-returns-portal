from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    SelectField
)
from wtforms.fields import TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms.validators import (
    InputRequired,
    DataRequired,
    Length,
    Email
)


class LoginForm(FlaskForm):
    """
    A class to be used with flask-wtf and wtforms to generate a Log In form
    to be used by visitors that have obtained a key from Curative directly.

    :param
        FlaskForm: An instance of a FlaskForm from flask_wtf.

    :returns
        A wtforms 'form' object that can be supplied to the positional arguments
        of the `jinja2 render_template` function
    """

    password = PasswordField('Password',
                             validators=[InputRequired(),
                                         DataRequired(),
                                         Length(min=8, max=20)])
    login = SubmitField('Log In')


class ShippingAddressForm(FlaskForm):
    """
        A class to be used with flask-wtf and wtforms to generate a Shipping Address
        form so that users can enter the address they are returning a test-kit from.

        :param
            FlaskForm: An instance of a FlaskForm from flask_wtf.

        :returns
            A wtforms 'form' object that can be supplied to the positional arguments
            of the `jinja2 render_template` function
    """

    name = StringField('Full Name', validators=[InputRequired(),
                                                DataRequired(),
                                                Length(min=2, max=25)])
    phone = StringField('Phone Number',
                        validators=[InputRequired(),
                                    DataRequired(),
                                    Length(min=9, max=12)])
    company_name = StringField('Company Name',
                               validators=[Length(min=1, max=25)])
    address_line_1 = StringField('Address Line 1', validators=[InputRequired(),
                                                               DataRequired(),
                                                               Length(min=2, max=60)])
    address_line_2 = StringField('Address Line 2', validators=[Length(max=60)])
    address_line_3 = StringField('Address Line 3', validators=[Length(max=60)])
    city_locality = StringField('City', validators=[InputRequired(),
                                                    DataRequired(),
                                                    Length(min=2, max=50)])
    state_province = StringField('State (2 character abbreviation)', validators=[InputRequired(),
                                                      DataRequired(),
                                                      Length(min=1, max=2)])
    postal_code = StringField('Postal Code', validators=[InputRequired(),
                                                         DataRequired(),
                                                         Length(min=1, max=15)])
    country_code = StringField("Country (2 character abbreviation)", validators=[InputRequired(),
                                                                                 DataRequired(),
                                                                                 Length(min=1, max=2)])
    address_residential_indicator = SelectField('Residential Address?',
                                                choices=["unknown", "yes", "no"])
    number_of_tests_to_return = StringField('# of tests you are returning',
                                            validators=[InputRequired(),
                                                        DataRequired(),
                                                        Length(min=1, max=10)])
    return_destination = SelectField('Curative Return Lab', choices=["DC Lab", "San Dimas Lab"])

    create_return_label = SubmitField('Create Label')


class SchedulePickupForm(FlaskForm):
    label_id = StringField('Label ID', validators=[InputRequired(),
                                                   DataRequired()])
    contact_name = StringField('Full Name', validators=[InputRequired(),
                                                        DataRequired()])
    contact_email = EmailField('Email',
                               validators=[InputRequired(),
                                           DataRequired(),
                                           Email()])
    contact_phone = StringField('Phone Number', validators=[InputRequired(),
                                                            DataRequired()])
    pickup_notes = TextAreaField('Pickup Notes', validators=[InputRequired(),
                                                             DataRequired()])
    schedule_pickup = SubmitField('Schedule Pickup')
    # pickup_window
