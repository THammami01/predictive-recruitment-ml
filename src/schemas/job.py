from marshmallow import Schema, fields, validate


class JobSchema(Schema):
    """
    Schema for representing a job.
    """

    title = fields.String(required=True)
    company = fields.String(required=True)
    workspace_type = fields.String(
        required=True, validate=validate.OneOf(["On-site", "Hybrid", "Remote"])
    )
    location = fields.String(required=True)
    type = fields.String(
        required=True,
        validate=validate.OneOf(
            ["Full-time", "Part-time", "Contract", "Internship", "Other"]
        ),
    )
    description = fields.String(required=True)
    email = fields.Email(required=True)


schema = JobSchema()
