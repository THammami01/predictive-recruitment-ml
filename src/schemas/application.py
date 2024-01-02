from marshmallow import Schema, fields, validate


class ApplicationSchema(Schema):
    """
    Schema for representing a job application.
    """

    name = fields.String(required=True, validate=validate.Length(min=1))
    years_of_experience = fields.Integer(required=True, validate=validate.Range(min=0))
    has_diploma = fields.Boolean(required=True)
    salary = fields.Integer(required=True, validate=validate.Range(min=0))
    email = fields.Email(required=True)
    cv_url = fields.Url(required=True)


schema = ApplicationSchema()
