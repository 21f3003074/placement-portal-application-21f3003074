<template>

    <AppNavbar

    role="admin"
    username="Administrator"
    :activeSection="activeSection"
    @change-section="activeSection = $event"
    />

    <div class="container pt-5" style="margin-top: 20px;">

        <div v-if="activeSection === 'home'">

            <div class="card shadow mb-3">

                <div class="card-body">

                    <h2 class="fw-bold">

                        Welcome Back, Administrator

                    </h2>

                    <p class="text-muted mb-0">

                        Manage students, companies, placement drives and monitor the complete recruitment process.

                    </p>

                </div>

            </div>

            <div class="row">

                <div class="col-md-3 mb-3">

                    <div class="card shadow text-center"
                        style="cursor: pointer;"
                        @click="activeSection = 'students'"
                    >

                        <div class="card-body">

                            <i class="bi bi-people-fill fs-1 text-primary"></i>

                            <h5>Total Students</h5>

                            <h2>{{ dashboard.total_students }}</h2>

                        </div>

                    </div>

                </div>

                <div class="col-md-3 mb-3">

                    <div class="card shadow text-center"
                        style="cursor: pointer;"
                        @click="activeSection = 'companies'"
                    >

                        <div class="card-body">

                            <i class="bi bi-building-fill fs-1 text-primary"></i>

                            <h5>Total Companies</h5>

                            <h2>{{ dashboard.total_companies }}</h2>

                        </div>

                    </div>

                </div>

                <div class="col-md-3 mb-3">

                    <div class="card shadow text-center"
                        style="cursor: pointer;"
                        @click="activeSection = 'drives'"
                    >

                        <div class="card-body">

                            <i class="bi bi-briefcase-fill fs-1 text-primary"></i>

                            <h5>Total Drives</h5>

                            <h2>{{ dashboard.total_drives }}</h2>

                        </div>

                    </div>

                </div>

                <div class="col-md-3 mb-3">

                    <div class="card shadow text-center"
                        style="cursor: pointer;"
                        @click="activeSection = 'applications'"
                    >

                        <div class="card-body">

                            <i class="bi bi-file-earmark-check-fill fs-1 text-primary"></i>

                            <h5>Total Applications</h5>

                            <h2>{{ dashboard.total_applications }}</h2>

                        </div>

                    </div>

                </div>

            </div>

            <div class="row mt-3">

                <div class="col-md-4">

                    <div class="card border-warning">

                        <div class="card-body text-center"
                            style="cursor: pointer;"
                            @click="activeSection = 'applications'"
                        >

                            <i class="bi bi-building-fill fs-1 text-warning"></i>

                            <h6>Pending Companies</h6>

                            <h3>{{ dashboard.pending_companies }}</h3>

                        </div>

                    </div>

                </div>

                <div class="col-md-4">

                    <div class="card border-warning">

                        <div class="card-body text-center"
                            style="cursor: pointer;"
                            @click="activeSection = 'applications'"             
                        >

                            <i class="bi bi-briefcase-fill fs-1 text-warning"></i>

                            <h6>Pending Drives</h6>

                            <h3>{{ dashboard.pending_drives }}</h3>

                        </div>

                    </div>

                </div>

                <div class="col-md-4">

                    <div class="card border-success">

                        <div class="card-body text-center"
                            style="cursor: pointer;"
                            @click="activeSection = 'applications'"
                        >

                            <i class="bi bi-people-fill fs-1 text-success"></i>

                            <h6>Selected Students</h6>

                            <h3>{{ dashboard.selected_students }}</h3>

                        </div>

                    </div>

                </div>

            </div>

            <div class="row mt-4 mb-4">

                <div class="col-md-6 mb-3">

                    <div class="card shadow">

                        <div class="card-header fw-bold">

                            Pending Company Approvals

                        </div>

                        <ul class="list-group list-group-flush">

                            <li
                                class="list-group-item"
                                v-for="company in pendingCompanies.slice(0,5)"
                                :key="company.company_id"
                            >

                                {{ company.company_name }}

                            </li>

                        </ul>

                    </div>

                </div>

                <div class="col-md-6 mb-3">

                    <div class="card shadow">

                        <div class="card-header fw-bold">

                            Pending Placement Drives

                        </div>

                        <ul class="list-group list-group-flush">

                            <li
                                class="list-group-item"
                                v-for="drive in pendingDrives.slice(0,5)"
                                :key="drive.drive_id"
                            >

                                {{ drive.company_name }} - {{ drive.job_title }}

                            </li>

                        </ul>

                    </div>

                </div>

            </div>

        </div>

        <div v-if="activeSection === 'companies'">

            <div class="d-flex justify-content-between align-items-center mb-4">

                <h3 class = "mb-4">

                    Company Management

                </h3>

            </div>

            <div class="row mb-3">

                <div class="col-md-8">

                    <input

                        type="text"

                        class="form-control"

                        placeholder="Search by Company Name or HR Name"

                        v-model="companySearch"

                    >

                </div>

            </div>

            <h5 class="mb-3">

                Pending Company Approvals

            </h5>

            <table class="table table-bordered">

                <thead>

                    <tr>

                        <th>Company</th>

                        <th>HR Contact (Name)</th>

                        <th>Website</th>

                        <th>Status</th>

                        <th>Actions</th>

                    </tr>

                </thead>

                <tbody>

                    <tr

                        v-for="company in filteredPendingCompanies"

                        :key="company.company_id"

                    >

                        <td>

                            {{ company.company_name }}

                        </td>

                        <td>

                            {{ company.hr_contact_name }}

                        </td>

                        <td>

                            <a

                                :href="company.website"

                                target="_blank"

                            >

                                {{ company.website }}

                            </a>

                        </td>

                        <td>

                            <span

                                v-if="company.approval_status==='approved'"

                                class="badge bg-success"

                            >

                                Approved

                            </span>

                            <span

                                v-else-if="company.approval_status==='pending'"

                                class="badge bg-warning text-dark"

                            >

                                Pending

                            </span>

                            <span

                                v-else

                                class="badge bg-danger"

                            >

                                Rejected

                            </span>

                        </td>

                        <td>

                            <button

                                class="btn btn-success btn-sm me-2"
                                @click="approveCompany(company.company_id)"

                            >

                                Approve

                            </button>

                            <button

                                class="btn btn-danger btn-sm"
                                @click="rejectCompany(company.company_id)"

                            >

                                Reject

                            </button>

                        </td>

                    </tr>

                    <tr v-if="filteredPendingCompanies.length === 0">

                        <td colspan="5" class="text-center text-muted">

                            No Pending Company Approvals

                        </td>

                    </tr>

                </tbody>

            </table>

            <hr class="my-5">

            <h5 class="mb-3">

                All Registered Companies

            </h5>

            <table class="table table-bordered table-hover">

                <thead>

                    <tr>

                        <th>Company</th>

                        <th>HR Contact (Name)</th>

                        <th>Website</th>

                        <th>Approval</th>

                        <th>Account</th>

                        <th>Action</th>

                    </tr>

                </thead>

                <tbody>

                    <tr

                        v-for="company in filteredCompanies"

                        :key="company.company_id"

                    >

                        <td>

                            {{ company.company_name }}

                        </td>

                        <td>

                            {{ company.hr_contact_name }}

                        </td>

                        <td>

                            <a

                                :href="company.website"

                                target="_blank"

                            >

                                {{ company.website }}

                            </a>

                        </td>

                        <td>

                            <span

                                v-if="company.approval_status==='approved'"

                                class="badge bg-success"

                            >

                                Approved

                            </span>

                            <span

                                v-else-if="company.approval_status==='pending'"

                                class="badge bg-warning text-dark"

                            >

                                Pending

                            </span>

                            <span

                                v-else

                                class="badge bg-danger"

                            >

                                Rejected

                            </span>

                        </td>

                        <td>

                            <span

                                v-if="company.active"

                                class="badge bg-success"

                            >

                                Active

                            </span>

                            <span

                                v-else

                                class="badge bg-secondary"

                            >

                                Disabled

                            </span>

                        </td>

                        <td>

                            <button

                                v-if="company.approval_status === 'approved' && company.active"

                                class="btn btn-danger btn-sm"

                                @click="deactivateCompany(company.user_id)"

                            >

                                Deactivate

                            </button>

                            <button

                                v-else-if="company.approval_status === 'approved' && !company.active"

                                class="btn btn-success btn-sm"

                                @click="activateCompany(company.user_id)"

                            >

                                Activate

                            </button>

                            <button

                                v-else-if="company.approval_status === 'pending'"

                                class="btn btn-secondary btn-sm"

                                disabled

                            >

                                Deactivate

                            </button>

                            <button

                                v-else

                                class="btn btn-secondary btn-sm"

                                disabled

                            >

                                Deactivate

                            </button>

                        </td>

                    </tr>

                    <tr v-if="filteredCompanies.length === 0">

                        <td colspan="6" class="text-center text-muted">

                            No Companies Found

                        </td>

                    </tr>

                </tbody>

            </table>

        </div>

        <div v-if="activeSection === 'drives'">

            <h3 class="mb-4">

                Drive Management

            </h3>

            <div class="row mb-3">

                <div class="col-md-8">

                    <input

                        type="text"

                        class="form-control"

                        placeholder="Search by Company or Job Title"

                        v-model="driveSearch"

                    >

                </div>

            </div>

            <h5 class="mb-3">

                Pending Placement Drives

            </h5>

            <table class="table table-bordered">

                <thead>

                    <tr>

                        <th>Company</th>
                        <th>Job Title</th>
                        <th>Branch</th>
                        <th>CGPA</th>
                        <th>Year</th>
                        <th>Status</th>
                        <th>Action</th>

                    </tr>

                </thead>

                <tbody>

                    <tr

                        v-for="drive in filteredPendingDrives"

                        :key="drive.drive_id"

                    >

                        <td>{{ drive.company_name }}</td>

                        <td>{{ drive.job_title }}</td>

                        <td>{{ drive.eligibility_branch }}</td>

                        <td>{{ drive.eligibility_cgpa }}</td>

                        <td>{{ drive.eligibility_year }}</td>

                        <td>

                            <span

                                class="badge bg-warning text-dark"

                            >

                                Pending

                            </span>

                        </td>

                        <td>

                            <button
                                class="btn btn-success btn-sm me-2"
                                @click="approveDrive(drive.drive_id)"
                            >
                                Approve
                            </button>

                            <button
                                class="btn btn-danger btn-sm"
                                @click="rejectDrive(drive.drive_id)"
                            >
                                Reject
                            </button>

                        </td>

                    </tr>

                    <tr v-if="filteredPendingDrives.length === 0">

                        <td colspan="7" class="text-center text-muted">

                            No Pending Placement Drives

                        </td>

                    </tr>

                </tbody>

            </table>

            <hr class="my-5">

            <h5 class="mb-3">

                All Placement Drives

            </h5>

            <table class="table table-bordered">

                <thead>

                    <tr>

                        <th>Company</th>
                        <th>Job Title</th>
                        <th>Status</th>
                        <th>Applicants</th>
                        <th>Deadline</th>
                        <th>Action</th>

                    </tr>

                </thead>

                <tbody>

                    <tr

                        v-for="drive in filteredDrives"

                        :key="drive.drive_id"

                    >

                        <td>{{ drive.company_name }}</td>

                        <td>{{ drive.job_title }}</td>

                        <td>

                            <span

                                v-if="drive.status === 'approved'"

                                class="badge bg-success"

                            >

                                Approved

                            </span>

                            <span

                                v-else-if="drive.status === 'pending'"

                                class="badge bg-warning text-dark"

                            >

                                Pending

                            </span>

                            <span

                                v-else-if="drive.status === 'closed'"

                                class="badge bg-secondary"

                            >

                                Closed

                            </span>

                            <span

                                v-else

                                class="badge bg-danger"

                            >

                                Rejected

                            </span>

                        </td>

                        <td>{{ drive.applicant_count }}</td>

                        <td>{{ drive.application_deadline }}</td>

                        <td>

                            <button

                                class="btn btn-primary btn-sm"

                                data-bs-toggle="modal"

                                data-bs-target="#driveDetailsModal"

                                @click="viewDrive(drive)"

                            >

                                <i class="bi bi-eye-fill me-1"></i>

                                View

                            </button>

                        </td>

                    </tr>

                    <tr v-if="filteredDrives.length === 0">

                        <td colspan="6" class="text-center text-muted">

                            No Placement Drives Found

                        </td>

                    </tr>

                </tbody>

            </table>

        </div>

        <div v-if="activeSection === 'students'">

            <h3 class="mb-4">

                Student Management

            </h3>

            <div class="row mb-3">

                <div class="col-md-8">

                    <input

                        type="text"

                        class="form-control"

                        placeholder="Search by Student Name, Email or Branch"

                        v-model="studentSearch"

                    >

                </div>

            </div>

            <table class="table table-bordered">

                    <thead>

                        <tr>

                            <th>Name</th>

                            <th>Email</th>

                            <th>Branch</th>

                            <th>CGPA</th>

                            <th>Year</th>

                            <th>Resume</th>

                            <th>Account</th>

                            <th>Action</th>

                        </tr>

                    </thead>

                    <tbody>

                        <tr

                            v-for="student in filteredStudents"

                            :key="student.student_id"

                        >

                            <td>

                                {{ student.name }}

                            </td>

                            <td>

                                {{ student.email }}

                            </td>

                            <td>

                                {{ student.branch }}

                            </td>

                            <td>

                                {{ student.cgpa }}

                            </td>

                            <td>

                                {{ student.graduation_year }}

                            </td>

                            <td>

                                <a

                                    v-if="student.resume"

                                    :href="'http://127.0.0.1:5000/' + student.resume"

                                    target="_blank"

                                    class="btn btn-primary btn-sm"

                                >

                                    <i class="bi bi-file-earmark-pdf me-1"></i>

                                    View Resume

                                </a>

                                <span

                                    v-else

                                    class="text-muted"

                                >

                                    Not Uploaded

                                </span>

                            </td>

                            <td>

                                <span

                                    v-if="student.active"

                                    class="badge bg-success"

                                >

                                    Active

                                </span>

                                <span

                                    v-else

                                    class="badge bg-secondary"

                                >

                                    Disabled

                                </span>

                            </td>

                            <td>

                                <button

                                    v-if="student.active"

                                    class="btn btn-danger btn-sm"

                                    @click="deactivateStudent(student.student_id)"

                                >
                                    Deactivate

                                </button>

                                <button

                                    v-else

                                    class="btn btn-success btn-sm"

                                    @click="activateStudent(student.student_id)"

                                >

                                    Activate

                                </button>
                            </td>

                        </tr>

                        <tr v-if="filteredStudents.length === 0">

                            <td colspan="7" class="text-center text-muted">

                                No Students Found

                            </td>

                        </tr>

                    </tbody>

            </table>

        </div>

        <div v-if="activeSection === 'applications'">

            <h3 class="mb-4">

                Application Management

            </h3>

            <div class="row mb-3">

                <div class="col-md-6">

                    <input

                        type="text"

                        class="form-control"

                        placeholder="Search Student, Company or Job"

                        v-model="applicationSearch"

                    >

                </div>

                <div class="col-md-3">

                    <select

                        class="form-select"

                        v-model="applicationStatus"

                    >

                        <option value="">

                            All Status

                        </option>

                        <option value="applied">

                            Applied

                        </option>

                        <option value="shortlisted">

                            Shortlisted

                        </option>

                        <option value="interview">

                            Interview

                        </option>

                        <option value="selected">

                            Selected

                        </option>

                        <option value="rejected">

                            Rejected

                        </option>

                    </select>

                </div>

            </div>

            <h5 class="mb-3">

                All Student Applications

            </h5>

            <table class="table table-bordered">

                <thead>

                    <tr>

                        <th>Student</th>

                        <th>Email</th>

                        <th>Company</th>

                        <th>Job</th>

                        <th>Status</th>

                        <th>Applied On</th>

                    </tr>

                </thead>

                <tbody>

                    <tr

                        v-for="application in filteredApplications"

                        :key="application.application_id"

                    >

                        <td>

                            {{ application.student_name }}

                        </td>

                        <td>

                            {{ application.student_email }}

                        </td>

                        <td>

                            {{ application.company_name }}

                        </td>

                        <td>

                            {{ application.job_title }}

                        </td>

                        <td>

                            <span

                                v-if="application.status==='applied'"

                                class="badge bg-primary"

                            >

                                Applied

                            </span>

                            <span

                                v-else-if="application.status==='shortlisted'"

                                class="badge bg-warning text-dark"

                            >

                                Shortlisted

                            </span>

                            <span

                                v-else-if="application.status==='interview'"

                                class="badge bg-info text-dark"

                            >

                                Interview

                            </span>

                            <span

                                v-else-if="application.status==='selected'"

                                class="badge bg-success"

                            >

                                Selected

                            </span>

                            <span

                                v-else

                                class="badge bg-danger"

                            >

                                Rejected

                            </span>

                        </td>

                        <td>

                            {{ application.application_date }}

                        </td>

                    </tr>

                    <tr v-if="filteredApplications.length===0">

                        <td colspan="6" class="text-center text-muted">

                            No Applications Found

                        </td>

                    </tr>

                </tbody>

            </table>

        </div>

    </div>

    <div

        class="modal fade"

        id="driveDetailsModal"

        tabindex="-1"

    >

        <div class="modal-dialog modal-lg">

            <div class="modal-content">

                <div class="modal-header">

                    <h5 class="modal-title">

                        Placement Drive Details

                    </h5>

                    <button

                        type="button"

                        class="btn-close"

                        data-bs-dismiss="modal"

                    ></button>

                </div>

                <div

                    class="modal-body"

                    v-if="selectedDrive"

                >

                    <div class="row">

                        <div class="col-md-6 mb-3">

                            <label class="form-label">

                                Company

                            </label>

                            <input

                                class="form-control"

                                :value="selectedDrive.company_name"

                                readonly

                            >

                        </div>

                        <div class="col-md-6 mb-3">

                            <label class="form-label">

                                Job Title

                            </label>

                            <input

                                class="form-control"

                                :value="selectedDrive.job_title"

                                readonly

                            >

                        </div>

                    </div>

                    <div class="mb-3">

                        <label class="form-label">

                            Job Description

                        </label>

                        <textarea

                            class="form-control"

                            rows="4"

                            :value="selectedDrive.job_description"

                            readonly

                        ></textarea>

                    </div>

                    <div class="row">

                        <div class="col-md-6 mb-3">

                            <label class="form-label">

                                Eligible Branches

                            </label>

                            <input

                                class="form-control"

                                :value="selectedDrive.eligibility_branch"

                                readonly

                            >

                        </div>

                        <div class="col-md-3 mb-3">

                            <label class="form-label">

                                Minimum CGPA

                            </label>

                            <input

                                class="form-control"

                                :value="selectedDrive.eligibility_cgpa"

                                readonly

                            >

                        </div>

                        <div class="col-md-3 mb-3">

                            <label class="form-label">

                                Graduation Year

                            </label>

                            <input

                                class="form-control"

                                :value="selectedDrive.eligibility_year"

                                readonly

                            >

                        </div>

                    </div>

                    <div class="row">

                        <div class="col-md-4 mb-3">

                            <label class="form-label">

                                Deadline

                            </label>

                            <input

                                class="form-control"

                                :value="selectedDrive.application_deadline"

                                readonly

                            >

                        </div>

                        <div class="col-md-4 mb-3">

                            <label class="form-label">

                                Applicants

                            </label>

                            <input

                                class="form-control"

                                :value="selectedDrive.applicant_count"

                                readonly

                            >

                        </div>

                        <div class="col-md-4 mb-3">

                            <label class="form-label">

                                Status

                            </label>

                            <input

                                class="form-control"

                                :value="selectedDrive.status"

                                readonly

                            >

                        </div>

                    </div>

                </div>

                <div class="modal-footer">

                    <button

                        class="btn btn-secondary"

                        data-bs-dismiss="modal"

                    >

                        Close

                    </button>

                </div>

            </div>

        </div>

    </div>

</template>

<script setup>

import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import AppNavbar from "@/components/AppNavbar.vue"

const dashboard = ref({})
const pendingCompanies = ref([])
const pendingDrives = ref([])
const studentSearch = ref("")
const students = ref([])
const companySearch = ref("")
const companies = ref([])
const applications = ref([])
const activeSection = ref("home")
const driveSearch = ref("")
const drives = ref([])
const selectedDrive = ref(null)
const applicationSearch = ref("")
const applicationStatus = ref("")

onMounted(async () => {

    try {

        const response = await axios.get(

            "/admin-dashboard",

            {
                withCredentials: true
            }

        )

        dashboard.value = response.data

        await loadPendingCompanies()

        await loadPendingDrives()

        await loadApplications()

        await loadCompanies()

        await loadDrives()

        await searchStudents()

        console.log(dashboard.value)

    }

    catch (error) {

        console.log(error)

    }

})

const loadApplications = async () => {

    try {

        const response = await axios.get(

            "/admin/applications",

            {
                withCredentials: true
            }

        )

        applications.value = response.data

    }

    catch (error) {

        console.log(error)

    }

}

const loadCompanies = async()=>{

    try{

        const response = await axios.get(

            "/admin/companies",

            {

                withCredentials:true

            }

        )

        companies.value=response.data

    }

    catch(error){

        console.log(error)

    }

}

const loadDrives = async () => {

    try {

        const response = await axios.get(

            "/admin/drives",

            {

                withCredentials:true

            }

        )

        drives.value = response.data

    }

    catch(error){

        console.log(error)

    }

}

const loadPendingCompanies = async () => {

    try {

        const response = await axios.get(

            "/admin/pending-companies",

            {
                withCredentials: true
            }

        )

        pendingCompanies.value = response.data

        console.log(
            "Pending Companies:",
            pendingCompanies.value
        )

    }

    catch (error) {

        console.log(error)

    }

}

const approveCompany = async (companyId) => {

    try {

        const response = await axios.post(

            `/admin/approve-company/${companyId}`,

            {},

            {
                withCredentials: true
            }

        )

        alert(response.data.message)

        await loadPendingCompanies()

        await loadCompanies()

    }

    catch (error) {

        if (error.response) {

            alert(error.response.data.message)

        }

    }

}

const rejectCompany = async (companyId) => {

    try {

        const response = await axios.post(

            `/admin/reject-company/${companyId}`,

            {},

            {
                withCredentials: true
            }

        )

        alert(response.data.message)

        await loadPendingCompanies()

        await loadCompanies()

    }

    catch (error) {

        if (error.response) {

            alert(error.response.data.message)

        }

    }

}

const loadPendingDrives = async () => {

    try {

        const response = await axios.get(

            "/admin/pending-drives",

            {
                withCredentials: true
            }

        )

        pendingDrives.value = response.data

        console.log(
            "Pending Drives:",
            pendingDrives.value
        )

    }

    catch (error) {

        console.log(error)

    }

}

const approveDrive = async (driveId) => {

    try {

        const response = await axios.post(

            `/admin/approve-drive/${driveId}`,

            {},

            {
                withCredentials: true
            }

        )

        alert(response.data.message)

        await loadPendingDrives()

        await loadDrives()

    }

    catch (error) {

        if (error.response) {

            alert(error.response.data.message)

        }

    }

}

const rejectDrive = async (driveId) => {

    try {

        const response = await axios.post(

            `/admin/reject-drive/${driveId}`,

            {},

            {
                withCredentials: true
            }

        )

        alert(response.data.message)

        await loadPendingDrives()

        await loadDrives()

    }

    catch (error) {

        if (error.response) {

            alert(error.response.data.message)

        }

    }

}

const searchStudents = async () => {

    try {

        const response = await axios.get(

            "/admin/search/student",

            {
                params: {
                    name: studentSearch.value
                },

                withCredentials: true
            }

        )

        students.value = response.data

        console.log(students.value)

    }

    catch (error) {

        console.log(error)

    }

}

const deactivateStudent = async (studentId) => {

    try {

        const response = await axios.post(

            `/admin/deactivate/student/${studentId}`,

            {},

            {
                withCredentials: true
            }

        )

        alert(response.data.message)

        await searchStudents()

    }

    catch (error) {

        if (error.response) {

            alert(error.response.data.message)

        }

    }

}

const activateStudent = async (studentId) => {

    try {

        const response = await axios.post(

            `/admin/activate/student/${studentId}`,

            {},

            {
                withCredentials: true
            }

        )

        alert(response.data.message)

        await searchStudents()

    }

    catch (error) {

        if (error.response) {

            alert(error.response.data.message)

        }

    }

}

const searchCompanies = async () => {

    try {

        const response = await axios.get(

            "/admin/search/company",

            {
                params: {

                    name: companySearch.value

                },

                withCredentials: true

            }

        )

        companies.value = response.data

        console.log(companies.value)

    }

    catch (error) {

        console.log(error)

    }

}

const deactivateCompany = async (userId) => {

    try {

        const response = await axios.post(

            `/admin/deactivate/company/${userId}`,

            {},

            {
                withCredentials: true
            }

        )

        alert(response.data.message)

        await searchCompanies()

    }

    catch (error) {

        if (error.response) {

            alert(error.response.data.message)

        }

    }

}

const activateCompany = async (userId) => {

    try {

        const response = await axios.post(

            `/admin/activate/company/${userId}`,

            {},

            {
                withCredentials: true
            }

        )

        alert(response.data.message)

        await searchCompanies()

    }

    catch (error) {

        if (error.response) {

            alert(error.response.data.message)

        }

    }

}

const filteredPendingCompanies = computed(() => {

    const search = companySearch.value.toLowerCase()

    return pendingCompanies.value.filter((company) => {

        return (

            company.company_name.toLowerCase().includes(search) ||

            company.hr_contact_name.toLowerCase().includes(search)

        )

    })

})

const filteredCompanies = computed(() => {

    const search = companySearch.value.toLowerCase()

    return companies.value.filter((company) => {

        return (

            company.company_name.toLowerCase().includes(search) ||

            company.hr_contact_name.toLowerCase().includes(search)

        )

    })

})

const filteredPendingDrives = computed(() => {

    const search = driveSearch.value.toLowerCase()

    return pendingDrives.value.filter((drive) => {

        return (

            drive.company_name.toLowerCase().includes(search) ||

            drive.job_title.toLowerCase().includes(search)

        )

    })

})

const filteredDrives = computed(() => {

    const search = driveSearch.value.toLowerCase()

    return drives.value.filter((drive) => {

        return (

            drive.company_name.toLowerCase().includes(search) ||

            drive.job_title.toLowerCase().includes(search)

        )

    })

})

const viewDrive = (drive) => {

    selectedDrive.value = drive

}

const filteredApplications = computed(()=>{

    return applications.value.filter((application)=>{

        const search = applicationSearch.value.toLowerCase()

        const matchesSearch =

            application.student_name.toLowerCase().includes(search)

            ||

            application.company_name.toLowerCase().includes(search)

            ||

            application.job_title.toLowerCase().includes(search)

        const matchesStatus =

            applicationStatus.value === ""

            ||

            application.status === applicationStatus.value

        return matchesSearch && matchesStatus

    })

})

const filteredStudents = computed(() => {

    const search = studentSearch.value.toLowerCase()

    return students.value.filter((student) => {

        return (

            student.name.toLowerCase().includes(search)

            ||

            student.email.toLowerCase().includes(search)

            ||

            student.branch.toLowerCase().includes(search)

        )

    })

})
</script>

<style scoped>

.dashboard-card{

    transition:0.25s;

}

.dashboard-card:hover{

    transform:translateY(-5px);

    box-shadow:0 10px 20px rgba(0,0,0,.15);

}

</style>