import os
from flask import Flask, render_template, request, session, redirect, url_for, jsonify, send_from_directory
from controllers import db, cache
from models import User, Company, StudentProfile, PlacementDrive, Application, ExportJob
from flask_migrate import Migrate
from datetime import datetime, date
from werkzeug.utils import secure_filename
from tasks import export_applications_task, daily_reminder_task, monthly_report_task
from flask_mail import Mail, Message
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.secret_key = "placement_portal_secret"

app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = False

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///placement.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "s.specific1@gmail.com"
app.config["MAIL_PASSWORD"] = "sbrr qtoz hkon slix"

app.config["CACHE_TYPE"] = "RedisCache"
app.config["CACHE_REDIS_HOST"] = "localhost"
app.config["CACHE_REDIS_PORT"] = 6379
app.config["CACHE_DEFAULT_TIMEOUT"] = 60

ALLOWED_EXTENSIONS = {"pdf", "doc", "docx", "jpg", "jpeg", "png"}

db.init_app(app)
cache.init_app(app)
mail = Mail(app)
migrate = Migrate(app, db) #flask db init, #flask db migrate -m "msg", #flask db upgrade

with app.app_context():
    db.create_all()

@app.route("/")
def home():

    return jsonify({
        "message": "Placement Portal Backend Running"
    }), 200

@app.route("/admin")
def admin():

    user = User.query.filter_by(
        email="21f3003074@ds.study.iitm.ac.in"
    ).first()

    if not user:
        return jsonify({
            "message": "Admin Not Found"
        }), 404

    return jsonify({
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role
    }), 200


@app.route("/register", methods=["POST"])
def register():

    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]
    branch = request.form["branch"]
    cgpa = float(request.form["cgpa"])
    graduation_year = int(request.form["graduation_year"])

    if not name or not email or not password:
        return jsonify({
            "message": "Please Fill All Fields"
        }), 400

    existing_user = User.query.filter_by(
        email=email
    ).first()

    if existing_user:
        return jsonify({
            "message": "User Already Exists"
        }), 400

    student = User(
        name=name,
        email=email,
        password=password,
        role="student"
    )

    db.session.add(student)
    db.session.commit()

    profile = StudentProfile(
        user_id=student.id,
        branch=branch,
        cgpa=cgpa,
        graduation_year=graduation_year,
        resume=""
    )

    db.session.add(profile)
    db.session.commit()

    return jsonify({
        "message": "Student Registered Successfully",
        "user_id": student.id
    }), 201

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "GET":

        return jsonify({
            "message": "Login Endpoint Ready",
            "required_fields": [
                "email",
                "password"
            ]
        }), 200

    data = request.get_json()
    email = data["email"]
    password = data["password"]

    user = User.query.filter_by(
        email=email
    ).first()

    if not user:
        return jsonify({
            "message": "User Not Found. Please Register."
        }), 404

    if not user.active:
        return jsonify({
            "message": "Account Deactivated"
        }), 403

    if user.password != password:
        return jsonify({
            "message": "Incorrect Password"
        }), 401

    session["user_id"] = user.id
    session["role"] = user.role

    return jsonify({
        "message": f"Welcome {user.name}",
        "user_id": user.id,
        "role": user.role
    }), 200

@app.route("/admin-dashboard")
def admin_dashboard():

    if not session.get("user_id"):
        return jsonify({
            "message": "Please Login First"
        }), 401

    if session.get("role") != "admin":
        return jsonify({
            "message": "Access Denied"
        }), 403

    student_count = User.query.filter_by(
        role="student"
    ).count()

    company_count = User.query.filter_by(
        role="company"
    ).count()

    drive_count = PlacementDrive.query.count()

    application_count = Application.query.count()

    pending_company_count = Company.query.filter_by(
        approval_status="pending"
    ).count()

    pending_drive_count = PlacementDrive.query.filter_by(
        status="pending"
    ).count()

    selected_student_count = Application.query.filter_by(
        status="selected"
    ).count()

    return jsonify({
        "total_students": student_count,
        "total_companies": company_count,
        "total_drives": drive_count,
        "total_applications": application_count,
        "pending_companies": pending_company_count,
        "pending_drives": pending_drive_count,
        "selected_students": selected_student_count
    }), 200


@app.route("/student/dashboard")
def student_dashboard():

    if not session.get("user_id"):
        return jsonify({
            "message": "Please Login First"
        }), 401

    if session.get("role") != "student":
        return jsonify({
            "message": "Access Denied"
        }), 403

    user = User.query.get(
        session["user_id"]
    )

    application_count = Application.query.filter_by(
        student_id=session["user_id"]
    ).count()

    return jsonify({
        "message": f"Welcome {user.name}",
        "student_id": user.id,
        "name": user.name,
        "email": user.email,
        "application_count": application_count
    }), 200

@app.route("/company/dashboard")
def company_dashboard():

    if not session.get("user_id"):
        return jsonify({
            "message": "Please Login First"
        }), 401

    if session.get("role") != "company":
        return jsonify({
            "message": "Access Denied"
        }), 403

    user = User.query.get(
        session["user_id"]
    )

    company = Company.query.filter_by(
        user_id=session["user_id"]
    ).first()

    drives = PlacementDrive.query.filter_by(
        company_id=company.id
    ).all()

    total_applicants = 0
    shortlisted = 0
    selected = 0

    for drive in drives:

        applications = Application.query.filter_by(
            drive_id=drive.id
        ).all()

        total_applicants += len(applications)

        shortlisted += sum(
            application.status == "shortlisted"
            for application in applications
        )

        selected += sum(
            application.status == "selected"
            for application in applications
        )

    drive_count = PlacementDrive.query.filter_by(
        company_id=company.id
    ).count()

    return jsonify({
        "message": f"Welcome {user.name}",
        "company_id": company.id,
        "company_name": company.company_name,
        "approval_status": company.approval_status,
        "total_drives": drive_count,
        "total_applicants": total_applicants,
        "shortlisted": shortlisted,
        "selected": selected,
        "hr_contact_name": company.hr_contact_name,
        "website": company.website,
        "description": company.description
    }), 200

@app.route("/logout", methods=["POST"])
def logout():

    session.clear()

    return jsonify({
        "message": "Logged Out Successfully"
    }), 200

@app.route("/company-register", methods=["POST"])
def company_register():

    company_name = request.form["company_name"]
    hr_contact_name = request.form["hr_contact_name"]
    email = request.form["email"]
    password = request.form["password"]
    website = request.form["website"]
    description = request.form["description"]

    if (
        not company_name
        or not hr_contact_name
        or not email
        or not password
        or not description
    ):
        return jsonify({
            "message": "Please Fill All Required Fields"
        }), 400

    existing_user = User.query.filter_by(
        email=email
    ).first()

    if existing_user:
        return jsonify({
            "message": "Email Already Exists"
        }), 400

    try:

        user = User(
            name=company_name,
            email=email,
            password=password,
            role="company"
        )

        db.session.add(user)

        db.session.flush()

        company = Company(
            user_id=user.id,
            company_name=company_name,
            hr_contact_name=hr_contact_name,
            website=website,
            description=description,
            approval_status="pending"
        )

        db.session.add(company)

        db.session.commit()

        return jsonify({
            "message": "Company Registered Successfully",
            "company_id": company.id,
            "approval_status": company.approval_status
        }), 201

    except Exception as e:

        db.session.rollback()

        return jsonify({
            "message": str(e)
        }), 500
    
@app.route("/admin/pending-companies")
def pending_companies():

    if session.get("role") != "admin":
        return jsonify({
            "message": "Access Denied"
        }), 403

    companies = Company.query.filter_by(
        approval_status="pending"
    ).all()

    companies_data = []

    for company in companies:

        companies_data.append({
            "company_id": company.id,
            "company_name": company.company_name,
            "hr_contact_name": company.hr_contact_name,
            "website": company.website,
            "approval_status": company.approval_status,
            "description": company.description
        })

    return jsonify(companies_data), 200

@app.route("/admin/companies")
def all_companies():

    if session.get("role") != "admin":
        return jsonify({
            "message":"Access Denied"
        }),403

    companies = Company.query.all()

    companies_data = []

    for company in companies:

        user = User.query.get(
            company.user_id
        )

        companies_data.append({

            "company_id":company.id,

            "user_id":user.id,

            "company_name":company.company_name,

            "hr_contact_name":company.hr_contact_name,

            "website":company.website,

            "approval_status":company.approval_status,

            "active":user.active

        })

    return jsonify(companies_data),200

@app.route("/admin/drives")
def all_drives():

    if session.get("role") != "admin":
        return jsonify({
            "message": "Access Denied"
        }), 403

    drives = PlacementDrive.query.all()

    drives_data = []

    for drive in drives:

        company = Company.query.get(
            drive.company_id
        )

        applicant_count = Application.query.filter_by(
            drive_id=drive.id
        ).count()

        drives_data.append({

            "drive_id": drive.id,

            "company_id": company.id,

            "company_name": company.company_name,

            "job_title": drive.job_title,

            "job_description": drive.job_description,

            "eligibility_branch": drive.eligibility_branch,

            "eligibility_cgpa": drive.eligibility_cgpa,

            "eligibility_year": drive.eligibility_year,

            "application_deadline": str(
                drive.application_deadline
            ),

            "status": drive.status,

            "applicant_count": applicant_count

        })

    return jsonify(
        drives_data
    ), 200


@app.route("/admin/approve-company/<int:company_id>", methods=["POST"])
def approve_company(company_id):

    if session.get("role") != "admin":
        return jsonify({
            "message": "Access Denied"
        }), 403

    company = Company.query.get(
        company_id
    )

    if not company:
        return jsonify({
            "message": "Company Not Found"
        }), 404

    company.approval_status = "approved"

    db.session.commit()

    return jsonify({
        "message": "Company Approved",
        "company_id": company.id,
        "company_name": company.company_name,
        "approval_status": company.approval_status
    }), 200

@app.route("/admin/reject-company/<int:company_id>", methods=["POST"])
def reject_company(company_id):

    if session.get("role") != "admin":
        return jsonify({
            "message": "Access Denied"
        }), 403

    company = Company.query.get(
        company_id
    )

    if not company:
        return jsonify({
            "message": "Company Not Found"
        }), 404

    company.approval_status = "rejected"

    db.session.commit()

    return jsonify({
        "message": "Company Rejected",
        "company_id": company.id,
        "company_name": company.company_name,
        "approval_status": company.approval_status
    }), 200

@app.route("/company/drives")
def company_drives():

    if session.get("role") != "company":
        return jsonify({
            "message": "Access Denied"
        }), 403

    company = Company.query.filter_by(
        user_id=session["user_id"]
    ).first()

    if not company:
        return jsonify({
            "message": "Company Not Found"
        }), 404

    drives = PlacementDrive.query.filter_by(
        company_id=company.id
    ).all()

    drives_data = []

    for drive in drives:

        applicant_count = Application.query.filter_by(
            drive_id=drive.id
        ).count()

        drives_data.append({

            "drive_id": drive.id,

            "job_title": drive.job_title,

            "job_description": drive.job_description,

            "eligibility_branch": drive.eligibility_branch,

            "eligibility_cgpa": drive.eligibility_cgpa,

            "eligibility_year": drive.eligibility_year,

            "status": drive.status,

            "application_deadline": str(
                drive.application_deadline
            ),

            "applicant_count": applicant_count

        })

    return jsonify(drives_data), 200

@app.route("/company/create-drive", methods=["POST"])
def create_drive():

    if session.get("role") != "company":
        return jsonify({
            "message": "Access Denied"
        }), 403

    company = Company.query.filter_by(
        user_id=session["user_id"]
    ).first()

    if company.approval_status == "pending":
        return jsonify({
            "message": "Approval Pending"
        }), 403

    if company.approval_status == "rejected":
        return jsonify({
            "message": "Company Rejected"
        }), 403

    job_title = request.form["job_title"]

    job_description = request.form[
        "job_description"
    ]

    branches = request.form.getlist(
        "eligibility_branch"
    )

    eligibility_branch = ",".join(
        branches
    )

    eligibility_cgpa = float(
        request.form["eligibility_cgpa"]
    )

    eligibility_year = int(
        request.form["eligibility_year"]
    )

    application_deadline = datetime.strptime(
        request.form["application_deadline"],
        "%Y-%m-%d"
    ).date()

    drive = PlacementDrive(
        company_id=company.id,
        job_title=job_title,
        job_description=job_description,
        eligibility_branch=eligibility_branch,
        eligibility_cgpa=eligibility_cgpa,
        eligibility_year=eligibility_year,
        application_deadline=application_deadline,
        status="pending"
    )

    db.session.add(
        drive
    )

    db.session.commit()

    return jsonify({
        "message": "Placement Drive Created Successfully",
        "drive_id": drive.id,
        "job_title": drive.job_title,
        "eligibility_branch": drive.eligibility_branch,
        "status": drive.status
    }), 201

@app.route("/company/edit-drive/<int:drive_id>", methods=["POST"])
def edit_drive(drive_id):

    if session.get("role") != "company":
        return jsonify({
            "message": "Access Denied"
        }), 403

    company = Company.query.filter_by(
        user_id=session["user_id"]
    ).first()

    if company.approval_status == "pending":
        return jsonify({
            "message": "Approval Pending"
        }), 403

    if company.approval_status == "rejected":
        return jsonify({
            "message": "Company Rejected"
        }), 403

    drive = PlacementDrive.query.get(
        drive_id
    )

    if not drive:
        return jsonify({
            "message": "Drive Not Found"
        }), 404

    if drive.company_id != company.id:
        return jsonify({
            "message": "Access Denied"
        }), 403

    job_title = request.form["job_title"]

    job_description = request.form["job_description"]

    branches = request.form.getlist("eligibility_branch")

    eligibility_branch = ",".join(branches)

    eligibility_cgpa = float(
        request.form["eligibility_cgpa"]
    )

    eligibility_year = int(
        request.form["eligibility_year"]
    )

    application_deadline = datetime.strptime(
        request.form["application_deadline"],
        "%Y-%m-%d"
    ).date()

    drive.job_title = job_title
    drive.job_description = job_description
    drive.eligibility_branch = eligibility_branch    
    drive.eligibility_cgpa = eligibility_cgpa
    drive.eligibility_year = eligibility_year
    drive.application_deadline = application_deadline

    drive.status = "pending"

    db.session.commit()

    return jsonify({
    "message": "Placement Drive Updated. Waiting For Approval."
    }), 200

@app.route("/company/toggle-drive-status/<int:drive_id>", methods=["POST"])
def toggle_drive_status(drive_id):

    if session.get("role") != "company":
        return jsonify({
            "message": "Access Denied"
        }), 403

    drive = PlacementDrive.query.get(
        drive_id
    )

    if not drive:
        return jsonify({
            "message": "Drive Not Found"
        }), 404

    company = Company.query.filter_by(
        user_id=session["user_id"]
    ).first()

    if not company:
        return jsonify({
            "message": "Company Not Found"
        }), 404

    if drive.company_id != company.id:
        return jsonify({
            "message": "Access Denied"
        }), 403

    if drive.status == "approved":

        drive.status = "closed"

    elif drive.status == "closed":

        drive.status = "approved"

    db.session.commit()

    return jsonify({
        "message": "Drive Status Updated"
    }), 200

@app.route("/admin/pending-drives")
def pending_drives():

    if session.get("role") != "admin":
        return jsonify({
            "message": "Access Denied"
        }), 403

    drives = PlacementDrive.query.filter_by(
        status="pending"
    ).all()

    drives_data = []

    for drive in drives:

        company = Company.query.get(
            drive.company_id
        )

        drives_data.append({
            "drive_id": drive.id,
            "job_title": drive.job_title,
            "company_name": company.company_name,
            "eligibility_branch": drive.eligibility_branch,
            "eligibility_cgpa": drive.eligibility_cgpa,
            "eligibility_year": drive.eligibility_year,
            "application_deadline": str(
                drive.application_deadline
            ),
            "status": drive.status,
            "job_description": drive.job_description
        })

    return jsonify(
        drives_data
    ), 200


@app.route("/admin/approve-drive/<int:drive_id>", methods=["POST"])
def approve_drive(drive_id):

    if session.get("role") != "admin":
        return jsonify({
            "message": "Access Denied"
        }), 403

    drive = PlacementDrive.query.get(
        drive_id
    )

    if not drive:
        return jsonify({
            "message": "Drive Not Found"
        }), 404

    drive.status = "approved"

    db.session.commit()
    cache.clear()

    return jsonify({
        "message": "Drive Approved Successfully",
        "drive_id": drive.id,
        "job_title": drive.job_title,
        "status": drive.status
    }), 200

@app.route("/admin/reject-drive/<int:drive_id>", methods=["POST"])
def reject_drive(drive_id):

    if session.get("role") != "admin":
        return jsonify({
            "message": "Access Denied"
        }), 403

    drive = PlacementDrive.query.get(
        drive_id
    )

    if not drive:
        return jsonify({
            "message": "Drive Not Found"
        }), 404

    drive.status = "rejected"

    db.session.commit()
    cache.clear()

    return jsonify({
        "message": "Drive Rejected Successfully",
        "drive_id": drive.id,
        "job_title": drive.job_title,
        "status": drive.status
    }), 200

@app.route("/student/drives")
@cache.cached(timeout=60, key_prefix=lambda: f"student_drives_{session.get('user_id')}")
def student_drives():

    if session.get("role") != "student":
        return jsonify({
            "message": "Access Denied"
        }), 403
    
    student_profile = StudentProfile.query.filter_by(
        user_id=session["user_id"]
    ).first()

    drives = PlacementDrive.query.filter_by(
        status="approved"
    ).all()

    drives_data = []

    for drive in drives:

        eligible_branches = drive.eligibility_branch.split(",")

        eligible = (
            student_profile is not None
            and student_profile.branch in eligible_branches
            and student_profile.cgpa >= drive.eligibility_cgpa
            and student_profile.graduation_year == drive.eligibility_year
        )

        application = Application.query.filter_by(
            student_id=session["user_id"],
            drive_id=drive.id
        ).first()

        already_applied = application is not None

        drives_data.append({
            "id": drive.id,
            "job_title": drive.job_title,
            "eligibility_branch": drive.eligibility_branch,
            "eligibility_cgpa": drive.eligibility_cgpa,
            "eligibility_year": drive.eligibility_year,
            "application_deadline": str(drive.application_deadline),
            "company_name": drive.company.company_name,
            "eligible": eligible,
            "already_applied": already_applied,
            "is_deadline_over": date.today() > drive.application_deadline
        })
    return jsonify(drives_data)

@app.route("/apply/<int:drive_id>", methods=["POST"])
def apply_drive(drive_id):

    if session.get("role") != "student":
        return jsonify({
            "message": "Access Denied"
        }), 403

    drive = PlacementDrive.query.get(drive_id)

    if not drive:
        return jsonify({
            "message": "Drive Not Found"
        }), 404

    student_profile = StudentProfile.query.filter_by(
        user_id=session["user_id"]
    ).first()

    if not student_profile:
        return jsonify({
            "message": "Complete Profile First"
        }), 400

    if not student_profile.resume:
        return jsonify({
            "message": "Upload Resume First and Complete your profile"
        }), 400
    
    if not student_profile.branch:
        return jsonify({
            "message": "Complete Profile First"
        }), 400

    if student_profile.cgpa is None:
        return jsonify({
            "message": "Complete Profile First"
        }), 400

    if student_profile.graduation_year is None:
        return jsonify({
            "message": "Complete Profile First"
        }), 400
    
    if date.today() > drive.application_deadline:
        return jsonify({
            "message": "Application Deadline Has Passed"
        }), 400

    eligible_branches = (
    drive.eligibility_branch.split(","))

    if student_profile.branch not in eligible_branches:
        return jsonify({
            "message": "Branch Not Eligible"
        }), 400
    
    if student_profile.graduation_year != drive.eligibility_year:
        return jsonify({
            "message": "Graduation Year Not Eligible"
        }), 400

    if student_profile.cgpa < drive.eligibility_cgpa:
        return jsonify({
            "message": "CGPA Not Eligible"
        }), 400

    if drive.status != "approved":
        return jsonify({
            "message": "Drive Not Available"
        }), 400

    student_id = session["user_id"]

    existing_application = Application.query.filter_by(
    student_id=student_id,
    drive_id=drive_id
    ).first()
    
    if existing_application:
        return jsonify({
            "message": "Already Applied"
        }), 400

    application = Application(
        student_id=student_id,
        drive_id=drive_id,
        application_date=date.today(),
        status="applied"
    )

    db.session.add(application)
    db.session.commit()
    cache.delete(
        f"student_drives_{session['user_id']}"
    )
    return jsonify({
        "message": "Application Submitted Successfully"
    }), 200

@app.route("/company/applications")
def company_applications():

    if session.get("role") != "company":
        return jsonify({
            "message": "Access Denied"
        }), 403

    company = Company.query.filter_by(
        user_id=session["user_id"]
    ).first()

    if not company:
        return jsonify({
            "message": "Company Not Found"
        }), 404

    drives = PlacementDrive.query.filter_by(
        company_id=company.id
    ).all()

    applications_data = []

    for drive in drives:

        applications = Application.query.filter_by(
            drive_id=drive.id
        ).all()

        for application in applications:

            student = User.query.get(
                application.student_id
            )

            if not student:
                continue

            student_profile = StudentProfile.query.filter_by(
                user_id=student.id
            ).first()

            if student_profile:

                applications_data.append({
                    "application_id": application.id,
                    "student_id": student.id,
                    "student_name": student.name,
                    "student_email": student.email,
                    "branch": student_profile.branch,
                    "cgpa": student_profile.cgpa,
                    "graduation_year": student_profile.graduation_year,
                    "resume": student_profile.resume,
                    "drive_id": drive.id,
                    "job_title": drive.job_title,
                    "application_status": application.status,
                    "application_date": str(
                        application.application_date
                    )
                })

            else:

                applications_data.append({
                    "application_id": application.id,
                    "student_id": student.id,
                    "student_name": student.name,
                    "student_email": student.email,
                    "profile_completed": False,
                    "drive_id": drive.id,
                    "job_title": drive.job_title,
                    "application_status": application.status,
                    "application_date": str(
                        application.application_date
                    )
                })

    return jsonify(
        applications_data
    ), 200

@app.route("/company/shortlist/<int:application_id>", methods=["POST"])
def shortlist_student(application_id):

    if session.get("role") != "company":
        return jsonify({
            "message": "Access Denied"
        }), 403

    application = Application.query.get(
        application_id
    )

    if not application:
        return jsonify({
            "message": "Application Not Found"
        }), 404

    drive = PlacementDrive.query.get(
        application.drive_id
    )

    if not drive:
        return jsonify({
            "message": "Drive Not Found"
        }), 404

    company = Company.query.filter_by(
        user_id=session["user_id"]
    ).first()

    if drive.company_id != company.id:
        return jsonify({
            "message": "Access Denied"
        }), 403

    application.status = "shortlisted"

    db.session.commit()

    return jsonify({
        "message": "Student Shortlisted",
        "application_id": application.id,
        "drive_id": drive.id,
        "status": application.status
    }), 200

@app.route("/company/interview/<int:application_id>", methods=["POST"])
def schedule_interview(application_id):

    if session.get("role") != "company":
        return jsonify({
            "message": "Access Denied"
        }), 403

    application = Application.query.get(
        application_id
    )

    if not application:
        return jsonify({
            "message": "Application Not Found"
        }), 404

    drive = PlacementDrive.query.get(
        application.drive_id
    )

    if not drive:
        return jsonify({
            "message": "Drive Not Found"
        }), 404

    company = Company.query.filter_by(
        user_id=session["user_id"]
    ).first()

    if drive.company_id != company.id:
        return jsonify({
            "message": "Access Denied"
        }), 403

    application.status = "interview"

    db.session.commit()

    return jsonify({
        "message": "Interview Scheduled",
        "status": application.status
    }), 200

@app.route("/company/select/<int:application_id>", methods=["POST"])
def select_student(application_id):

    if session.get("role") != "company":
        return jsonify({
            "message": "Access Denied"
        }), 403

    application = Application.query.get(
        application_id
    )

    if not application:
        return jsonify({
            "message": "Application Not Found"
        }), 404

    drive = PlacementDrive.query.get(
        application.drive_id
    )

    if not drive:
        return jsonify({
            "message": "Drive Not Found"
        }), 404

    company = Company.query.filter_by(
        user_id=session["user_id"]
    ).first()

    if drive.company_id != company.id:
        return jsonify({
            "message": "Access Denied"
        }), 403

    application.status = "selected"

    db.session.commit()

    return jsonify({
        "message": "Student Selected",
        "application_id": application.id,
        "drive_id": drive.id,
        "status": application.status
    }), 200

@app.route("/company/reject/<int:application_id>", methods=["POST"])
def reject_student(application_id):

    if session.get("role") != "company":
        return jsonify({
            "message": "Access Denied"
        }), 403

    application = Application.query.get(
        application_id
    )

    if not application:
        return jsonify({
            "message": "Application Not Found"
        }), 404

    drive = PlacementDrive.query.get(
        application.drive_id
    )

    if not drive:
        return jsonify({
            "message": "Drive Not Found"
        }), 404

    company = Company.query.filter_by(
        user_id=session["user_id"]
    ).first()

    if drive.company_id != company.id:
        return jsonify({
            "message": "Access Denied"
        }), 403

    application.status = "rejected"

    db.session.commit()

    return jsonify({
        "message": "Student Rejected",
        "application_id": application.id,
        "drive_id": drive.id,
        "status": application.status
    }), 200

@app.route("/student/applications")
def student_applications():

    if session.get("role") != "student":
        return jsonify({
            "message": "Access Denied"
        }), 403

    applications = Application.query.filter_by(
        student_id=session["user_id"]
    ).all()

    applications_data = []

    for application in applications:

        drive = PlacementDrive.query.get(
            application.drive_id
        )

        if not drive:
            continue    #if drive is deleted nd applicn. exists then handle it r/t showing error

        applications_data.append({
            "application_id": application.id,
            "drive_id": drive.id,
            "company_name": drive.company.company_name,
            "job_title": drive.job_title,
            "status": application.status,
            "application_date": str(
                application.application_date
            )
        })

    return jsonify(applications_data)

@app.route("/student/profile", methods=["GET", "POST"])
def student_profile():

    if session.get("role") != "student":
        return jsonify({
            "message": "Access Denied"
        }), 403

    profile = StudentProfile.query.filter_by(
        user_id=session["user_id"]
    ).first()

    if request.method == "GET":

        user = User.query.get(
            session["user_id"]
        )

        if not profile:
            return jsonify({
                "message": "Profile Not Found"
            }), 404

        return jsonify({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "branch": profile.branch,
            "cgpa": profile.cgpa,
            "graduation_year": profile.graduation_year,
            "resume": profile.resume
        }), 200

    branch = request.form["branch"]

    cgpa = float(
        request.form["cgpa"]
    )

    graduation_year = int(
        request.form["graduation_year"]
    )

    resume_file = request.files.get(
        "resume"
    )

    if not profile:

        if resume_file and resume_file.filename == "":
            return jsonify({
                "message": "Resume Required"
            }), 400

        extension = resume_file.filename.rsplit(
            ".", 1
        )[1].lower()

        if extension not in ALLOWED_EXTENSIONS:
            return jsonify({
                "message": "Invalid File Type"
            }), 400

        filename = (
            f"{session['user_id']}_"
            f"{datetime.now().strftime('%Y%m%d%H%M%S')}_"
            f"{secure_filename(resume_file.filename)}"
        )

        filepath = os.path.join(
            "uploads",
            filename
        )

        resume_file.save(
            filepath
        )

        profile = StudentProfile(
            user_id=session["user_id"],
            branch=branch,
            cgpa=cgpa,
            graduation_year=graduation_year,
            resume=filepath
        )

        db.session.add(
            profile
        )

    else:

        profile.branch = branch
        profile.cgpa = cgpa
        profile.graduation_year = graduation_year

        if resume_file and resume_file.filename != "":

            extension = resume_file.filename.rsplit(
                ".", 1
            )[1].lower()

            if extension not in ALLOWED_EXTENSIONS:
                return jsonify({
                    "message": "Invalid File Type"
                }), 400

            if os.path.exists(
                profile.resume
            ):
                os.remove(
                    profile.resume
                )

            filename = (
                f"{session['user_id']}_"
                f"{datetime.now().strftime('%Y%m%d%H%M%S')}_"
                f"{secure_filename(resume_file.filename)}"
            )

            filepath = os.path.join(
                "uploads",
                filename
            )

            resume_file.save(
                filepath
            )

            profile.resume = filename

    db.session.commit()

    return jsonify({
        "message": "Profile Saved Successfully"
    }), 200

@app.route("/uploads/<path:filename>")
def uploaded_file(filename):

    return send_from_directory(

        "uploads",

        filename

    )

@app.route("/admin/search/student")
def search_student():

    if session.get("role") != "admin":
        return jsonify({
            "message": "Access Denied"
        }), 403

    name = request.args.get(
        "name",
        ""
    )

    students = User.query.filter(
        User.role == "student",
        User.name.ilike(f"%{name}%")
    ).all()

    students_data = []

    for student in students:

        profile = StudentProfile.query.filter_by(
            user_id=student.id
        ).first()

        students_data.append({

            "student_id": student.id,

            "name": student.name,

            "email": student.email,

            "active": student.active,

            "branch": profile.branch if profile else "-",

            "cgpa": profile.cgpa if profile else "-",

            "graduation_year": profile.graduation_year if profile else "-",

            "resume": profile.resume if profile else None

        })

    return jsonify(
        students_data
    ), 200

@app.route("/admin/search/company")
def search_company():

    if session.get("role") != "admin":
        return jsonify({
            "message": "Access Denied"
        }), 403

    name = request.args.get(
        "name",
        ""
    )

    companies = Company.query.filter(
        Company.company_name.ilike(
            f"%{name}%"
        )
    ).all()

    companies_data = []

    for company in companies:

        user = User.query.get(company.user_id)

        companies_data.append({
            "company_id": company.id,
            "user_id": user.id,
            "company_name": company.company_name,
            "hr_contact_name": company.hr_contact_name,
            "website": company.website,
            "approval_status": company.approval_status,
            "active": user.active
        })

    return jsonify(
        companies_data
    ), 200

@app.route("/admin/applications")
def admin_applications():

    if session.get("role") != "admin":
        return jsonify({
            "message": "Access Denied"
        }), 403

    applications = Application.query.all()

    applications_data = []

    for application in applications:

        student = User.query.get(
            application.student_id
        )

        drive = PlacementDrive.query.get(
            application.drive_id
        )

        company = Company.query.get(
            drive.company_id
        )

        applications_data.append({

            "application_id": application.id,

            "student_name": student.name,

            "student_email": student.email,

            "company_name": company.company_name,

            "job_title": drive.job_title,

            "application_date": str(
                application.application_date
            ),

            "status": application.status

        })

    return jsonify(
        applications_data
    ), 200

@app.route("/admin/deactivate/student/<int:user_id>", methods=["POST"])
def deactivate_student(user_id):

    if session.get("role") != "admin":
        return jsonify({
            "message": "Access Denied"
        }), 403

    student = User.query.get(
        user_id
    )

    if not student:
        return jsonify({
            "message": "Student Not Found"
        }), 404

    if student.role != "student":
        return jsonify({
            "message": "Invalid User"
        }), 400

    student.active = False

    db.session.commit()

    return jsonify({
        "message": "Student Deactivated",
        "user_id": student.id,
        "name": student.name,
        "active": student.active
    }), 200


@app.route("/admin/deactivate/company/<int:user_id>", methods=["POST"])
def deactivate_company(user_id):

    if session.get("role") != "admin":
        return jsonify({
            "message": "Access Denied"
        }), 403

    company_user = User.query.get(
        user_id
    )

    if not company_user:
        return jsonify({
            "message": "Company Not Found"
        }), 404

    if company_user.role != "company":
        return jsonify({
            "message": "Invalid User"
        }), 400

    company_user.active = False

    db.session.commit()

    return jsonify({
        "message": "Company Deactivated",
        "user_id": company_user.id,
        "name": company_user.name,
        "active": company_user.active
    }), 200

@app.route("/admin/activate/student/<int:user_id>", methods=["POST"])
def activate_student(user_id):

    if session.get("role") != "admin":
        return jsonify({
            "message": "Access Denied"
        }), 403

    student = User.query.get(
        user_id
    )

    if not student:
        return jsonify({
            "message": "Student Not Found"
        }), 404

    if student.role != "student":
        return jsonify({
            "message": "Invalid User"
        }), 400

    student.active = True

    db.session.commit()

    return jsonify({
        "message": "Student Activated",
        "user_id": student.id,
        "name": student.name,
        "active": student.active
    }), 200


@app.route("/admin/activate/company/<int:user_id>", methods=["POST"])
def activate_company(user_id):

    if session.get("role") != "admin":
        return jsonify({
            "message": "Access Denied"
        }), 403

    company_user = User.query.get(
        user_id
    )

    if not company_user:
        return jsonify({
            "message": "Company Not Found"
        }), 404

    if company_user.role != "company":
        return jsonify({
            "message": "Invalid User"
        }), 400

    company_user.active = True

    db.session.commit()

    return jsonify({
        "message": "Company Activated",
        "user_id": company_user.id,
        "name": company_user.name,
        "active": company_user.active
    }), 200

@app.route("/student/export")
def export_applications():

    if session.get("role") != "student":
        return jsonify({
            "message": "Access Denied"
        }), 403

    job = ExportJob(
        student_id=session["user_id"]
    )

    db.session.add(
        job
    )

    db.session.commit()

    export_applications_task.delay(
        job.id
    )

    return jsonify({
        "message": "Export Started",
        "job_id": job.id,
        "status": job.status
    }), 202


@app.route("/student/exports")
def student_exports():

    if session.get("role") != "student":
        return jsonify({
            "message": "Access Denied"
        }), 403

    jobs = ExportJob.query.filter_by(
        student_id=session["user_id"]
    ).all()

    jobs_data = []

    for job in jobs:

        jobs_data.append({
            "job_id": job.id,
            "status": job.status,
            "filename": job.filename
        })

    return jsonify(
        jobs_data
    ), 200

@app.route("/exports/<path:filename>")
def download_export(filename):

    return send_from_directory(

        "exports",

        filename,

        as_attachment=True

    )

if __name__ == "__main__":
    app.run(debug=True)