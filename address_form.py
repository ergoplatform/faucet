from wtforms import Form, validators, StringField, SubmitField


class AddressForm(Form):
    """Address Form."""

    name = StringField('Address', validators=[validators.DataRequired(message=("Don't be shy!"))])
