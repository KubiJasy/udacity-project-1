from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SelectField,SelectMultipleField, DateTimeField, BooleanField, ValidationError
from wtforms.validators import DataRequired, AnyOf, URL, Optional, Length


class ShowForm(Form):
    artist_id = StringField(
        'artist_id', validators=[DataRequired(message="A show date must be added")]
    )
    venue_id = StringField(
        'venue_id', validators=[DataRequired(message="A show date must be added")]
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired(message="A show date must be added")],
        default= datetime.today()
    )

class VenueForm(Form):
    def validate_phone(form, field):
        if len(field.data) > 16:
            raise ValidationError('Phone number is too long.')
        try:
            number = int(field.data)
        except:
            raise ValidationError('Please enter a valid phone number')

    name = StringField(
        'name', validators=[DataRequired(message='Name required')]
    )
    city = StringField(
        'city', validators=[DataRequired(message='City required')]
    )
    state = SelectField(
        'state', validators=[DataRequired(message='State required')],
        choices=[
            ('AL', 'AL'),
            ('AK', 'AK'),
            ('AZ', 'AZ'),
            ('AR', 'AR'),
            ('CA', 'CA'),
            ('CO', 'CO'),
            ('CT', 'CT'),
            ('DE', 'DE'),
            ('DC', 'DC'),
            ('FL', 'FL'),
            ('GA', 'GA'),
            ('HI', 'HI'),
            ('ID', 'ID'),
            ('IL', 'IL'),
            ('IN', 'IN'),
            ('IA', 'IA'),
            ('KS', 'KS'),
            ('KY', 'KY'),
            ('LA', 'LA'),
            ('ME', 'ME'),
            ('MT', 'MT'),
            ('NE', 'NE'),
            ('NV', 'NV'),
            ('NH', 'NH'),
            ('NJ', 'NJ'),
            ('NM', 'NM'),
            ('NY', 'NY'),
            ('NC', 'NC'),
            ('ND', 'ND'),
            ('OH', 'OH'),
            ('OK', 'OK'),
            ('OR', 'OR'),
            ('MD', 'MD'),
            ('MA', 'MA'),
            ('MI', 'MI'),
            ('MN', 'MN'),
            ('MS', 'MS'),
            ('MO', 'MO'),
            ('PA', 'PA'),
            ('RI', 'RI'),
            ('SC', 'SC'),
            ('SD', 'SD'),
            ('TN', 'TN'),
            ('TX', 'TX'),
            ('UT', 'UT'),
            ('VT', 'VT'),
            ('VA', 'VA'),
            ('WA', 'WA'),
            ('WV', 'WV'),
            ('WI', 'WI'),
            ('WY', 'WY'),
        ]
    )
    address = StringField(
        'address', validators=[DataRequired(message='Address must be filled')]
    )
    phone = StringField(
        'phone', validators=[Optional(), Length(min=10, message='Phone number too short')]
    )
    image_link = StringField(
        'image_link', validators=[Optional(), URL(message='Please enter a valid URL')]
    )
    genres = SelectMultipleField(
        # TODO implement enum restriction
        'genres', validators=[DataRequired()],
        choices=[], coerce=int
    )
    facebook_link = StringField(
        'facebook_link', validators=[Optional(), URL(message='Please enter a valid URL')]
    )
    website_link = StringField(
        'website_link', validators=[Optional(), URL(message='Please enter a valid URL')]
    )

    seeking_talent = BooleanField( 'seeking_talent' )

    seeking_description = StringField(
        'seeking_description'
    )



class ArtistForm(Form):
    def validate_phone(form, field):
        if len(field.data) > 16:
            raise ValidationError('Phone number is too long.')
        try:
            number = int(field.data)
        except:
            raise ValidationError('Please enter a valid phone number')

    name = StringField(
        'name', validators=[DataRequired(message='Name required')]
    )
    city = StringField(
        'city', validators=[DataRequired(message='City required')]
    )
    state = SelectField(
        'state', validators=[DataRequired(message='State required')],
        choices=[
            ('AL', 'AL'),
            ('AK', 'AK'),
            ('AZ', 'AZ'),
            ('AR', 'AR'),
            ('CA', 'CA'),
            ('CO', 'CO'),
            ('CT', 'CT'),
            ('DE', 'DE'),
            ('DC', 'DC'),
            ('FL', 'FL'),
            ('GA', 'GA'),
            ('HI', 'HI'),
            ('ID', 'ID'),
            ('IL', 'IL'),
            ('IN', 'IN'),
            ('IA', 'IA'),
            ('KS', 'KS'),
            ('KY', 'KY'),
            ('LA', 'LA'),
            ('ME', 'ME'),
            ('MT', 'MT'),
            ('NE', 'NE'),
            ('NV', 'NV'),
            ('NH', 'NH'),
            ('NJ', 'NJ'),
            ('NM', 'NM'),
            ('NY', 'NY'),
            ('NC', 'NC'),
            ('ND', 'ND'),
            ('OH', 'OH'),
            ('OK', 'OK'),
            ('OR', 'OR'),
            ('MD', 'MD'),
            ('MA', 'MA'),
            ('MI', 'MI'),
            ('MN', 'MN'),
            ('MS', 'MS'),
            ('MO', 'MO'),
            ('PA', 'PA'),
            ('RI', 'RI'),
            ('SC', 'SC'),
            ('SD', 'SD'),
            ('TN', 'TN'),
            ('TX', 'TX'),
            ('UT', 'UT'),
            ('VT', 'VT'),
            ('VA', 'VA'),
            ('WA', 'WA'),
            ('WV', 'WV'),
            ('WI', 'WI'),
            ('WY', 'WY'),
        ]
    )
    phone = StringField(
        'phone', validators=[Optional(), Length(min=10, message='Phone number too short')]
    )
    image_link = StringField(
        'image_link', validators=[Optional(), URL(message='Please enter a valid URL')]
    )
    genres = SelectMultipleField(
        'genres', validators=[DataRequired()],
        choices=[], coerce=int
     )
    facebook_link = StringField(
        'facebook_link', validators=[Optional(), URL(message='Please enter a valid URL')]
    )
    website_link = StringField(
        'website_link', validators=[Optional(), URL(message='Please enter a valid URL')]
    )

    seeking_venue = BooleanField( 'seeking_venue' )

    seeking_description = StringField(
            'seeking_description'
     )

