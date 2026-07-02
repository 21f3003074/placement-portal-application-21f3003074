from controllers import db
from datetime import datetime

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    active = db.Column(db.Boolean, default=True)
    
class Company(db.Model):

    __tablename__ = "companies"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"),nullable=False)
    company_name = db.Column(db.String(150), nullable=False)
    hr_contact_name = db.Column(db.String(100), nullable=False)
    website = db.Column(db.String(200))
    description = db.Column(db.Text, nullable=False)
    approval_status = db.Column(db.String(20), nullable=False, default="pending")

class StudentProfile(db.Model):

    __tablename__ = "student_profiles"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    branch = db.Column(db.String(100), nullable=False)
    cgpa = db.Column(db.Float, nullable=False)
    graduation_year = db.Column(db.Integer, nullable=False)
    resume = db.Column(db.String(255), nullable=False)
    
class PlacementDrive(db.Model):

    __tablename__ = "placement_drives"

    id = db.Column(db.Integer, primary_key=True)

    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=False)
    job_title = db.Column(db.String(150), nullable=False)
    job_description = db.Column(db.Text, nullable=False)
    eligibility_branch = db.Column(db.String(100), nullable=False)
    eligibility_cgpa = db.Column(db.Float, nullable=False)
    eligibility_year = db.Column(db.Integer, nullable=False)
    application_deadline = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="pending")
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)

class Application(db.Model):

    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    drive_id = db.Column(db.Integer, db.ForeignKey("placement_drives.id"), nullable=False)
    application_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="applied")

class ExportJob(db.Model):

    __tablename__ = "export_jobs"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    filename = db.Column( db.String(255))
    status = db.Column( db.String(20), nullable=False, default="pending")
    created_at = db.Column( db.DateTime, nullable=False, default=datetime.now)
