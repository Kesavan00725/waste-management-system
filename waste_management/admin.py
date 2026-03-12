"""
Admin registration is intentionally minimal since we use MongoEngine (not Django ORM).
Django Admin does not natively support MongoEngine documents.
Management is handled through the custom web UI instead.
"""
# No admin registrations needed — all CRUD via custom views/templates.
