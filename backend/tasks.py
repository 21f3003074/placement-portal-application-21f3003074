import csv
import os

from celery_config import celery
from config import create_app
from controllers import db
from models import User, StudentProfile, Application, PlacementDrive, Company, ExportJob
from datetime import date, timedelta
from flask_mail import Mail, Message

@celery.task
def export_applications_task(job_id):

    app = create_app()

    with app.app_context():

        job = ExportJob.query.get(job_id)

        if not job:
            return "Job Not Found"
        
        job.status = "processing"
        db.session.commit()

        student_id = job.student_id

        applications = Application.query.filter_by(
            student_id=student_id
        ).all()

        filename = f"applications_{student_id}.csv"

        filepath = os.path.join(
            "exports",
            filename
        )

        with open(
            filepath,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                "Student ID",
                "Company Name",
                "Drive Title",
                "Application Status",
                "Application Date"
            ])

            for application in applications:

                drive = PlacementDrive.query.get(
                    application.drive_id
                )

                company = Company.query.get(
                    drive.company_id
                )

                writer.writerow([
                    student_id,
                    company.company_name,
                    drive.job_title,
                    application.status,
                    application.application_date
                ])

        print(f"CSV Generated: {filepath}")

        job.filename = filename
        job.status = "completed"
        db.session.commit()

        return filename
    
@celery.task
def daily_reminder_task():

    app = create_app()

    mail = Mail(app)

    with app.app_context():
        print("Task Started")

        tomorrow = date.today() + timedelta(days=1)

        drives = PlacementDrive.query.filter_by(
            status="approved"
        ).all()

        print(f"Found {len(drives)} drives")

        for drive in drives:

            print(f"Checking drive {drive.job_title}")

            if drive.application_deadline != tomorrow:
                continue

            students = User.query.filter_by(
                role="student",
                active=True
            ).all()

            eligible_branches = (
                drive.eligibility_branch.split(",")
            )

            for student in students:

                profile = StudentProfile.query.filter_by(
                    user_id=student.id
                ).first()

                if not profile:
                    continue

                if profile.branch not in eligible_branches:
                    continue

                if profile.cgpa < drive.eligibility_cgpa:
                    continue

                if profile.graduation_year != drive.eligibility_year:
                    continue

                existing_application = (
                    Application.query.filter_by(
                        student_id=student.id,
                        drive_id=drive.id
                    ).first()
                )

                if existing_application:
                    continue

                msg = Message(
                    subject="Placement Drive Reminder",
                    sender=app.config["MAIL_USERNAME"],
                    recipients=[student.email]
                )

                msg.body = (
                    f"Dear {student.name},\n\n"
                    f"The placement drive for "
                    f"{drive.job_title} closes tomorrow.\n\n"
                    f"Please apply before the deadline."
                )

                mail.send(msg)

        return "Daily Reminder Completed"
    
@celery.task
def monthly_report_task():

    app = create_app()

    mail = Mail(app)

    with app.app_context():

        admin = User.query.filter_by(
            role="admin",
            active=True
        ).first()

        if not admin:
            return "Admin Not Found"

        drives_count = PlacementDrive.query.filter_by(
            status="approved"
        ).count()

        applications_count = Application.query.count()

        selected_count = Application.query.filter_by(
            status="selected"
        ).count()

        html_report = f"""
        <h2>Monthly Placement Activity Report</h2>

        <table border="1" cellpadding="10">
            <tr>
                <th>Metric</th>
                <th>Count</th>
            </tr>

            <tr>
                <td>Approved Drives</td>
                <td>{drives_count}</td>
            </tr>

            <tr>
                <td>Total Applications</td>
                <td>{applications_count}</td>
            </tr>

            <tr>
                <td>Selected Students</td>
                <td>{selected_count}</td>
            </tr>
        </table>
        """

        msg = Message(
            subject="Monthly Placement Activity Report",
            sender=app.config["MAIL_USERNAME"],
            recipients=[admin.email]
        )

        msg.html = html_report

        mail.send(msg)

        print("Monthly Report Sent")

        return "Monthly Report Sent"