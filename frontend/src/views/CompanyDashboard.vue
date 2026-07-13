<template>

    <AppNavbar

        role="company"

        :username="dashboard.company_name"

        :activeSection="activeSection"

        @change-section="activeSection = $event"

    />

    <div class="container pt-5" style="margin-top: 20px;">

       <div v-if="activeSection === 'home'">

            <div class="card shadow-sm border-0 mb-3">

                <div class="card-body">

                    <h1 class="fw-bold">

                        Welcome Back, {{ dashboard.company_name }}

                    </h1>

                    <p class="text-muted mb-0">

                        Manage your placement drives and applicants.

                    </p>

                </div>

            </div>

            <div class="row g-4 mb-4">

                <div class="col-md-3">

                    <div
                        class="card shadow-sm text-center h-100 dashboard-card"
                        @click="activeSection='drives'"
                    >

                        <div class="card-body">

                            <i class="bi bi-briefcase fs-1 text-primary"></i>

                            <h5 class="mt-3">

                                Active Drives

                            </h5>

                            <h2>

                                {{ dashboard.total_drives }}

                            </h2>

                        </div>

                    </div>

                </div>

                <div class="col-md-3">

                    <div
                        class="card shadow-sm text-center h-100 dashboard-card"
                        @click="activeSection='applicants'"
                    >

                        <div class="card-body">

                            <i class="bi bi-people fs-1 text-success"></i>

                            <h5 class="mt-3">

                                Applicants

                            </h5>

                            <h2>

                                {{ dashboard.total_applicants }}

                            </h2>

                        </div>

                    </div>

                </div>

                <div class="col-md-3">

                    <div
                        class="card shadow-sm text-center h-100 dashboard-card"
                        @click="activeSection='applicants'"
                    >

                        <div class="card-body">

                            <i class="bi bi-check-circle fs-1 text-warning"></i>

                            <h5 class="mt-3">

                                Shortlisted

                            </h5>

                            <h2>

                                {{ dashboard.shortlisted }}

                            </h2>

                        </div>

                    </div>

                </div>

                <div class="col-md-3">

                    <div
                        class="card shadow-sm text-center h-100 dashboard-card"
                        @click="activeSection='applicants'"
                    >

                        <div class="card-body">

                            <i class="bi bi-trophy fs-1 text-danger"></i>

                            <h5 class="mt-3">

                                Selected

                            </h5>

                            <h2>

                                {{ dashboard.selected }}

                            </h2>

                        </div>

                    </div>

                </div>

            </div>

            <hr>

            <h3>

                Recent Placement Drives

            </h3>

            <div class="card shadow-sm border-0 mb-3">

                <table class="table table-bordered">

                    <thead>

                        <tr>

                            <th>Job Title</th>

                            <th>Status</th>

                            <th>Applicants</th>

                            <th>Deadline</th>

                        </tr>

                    </thead>

                    <tbody>

                        <tr

                            v-for="drive in filteredCompanyDrives"

                            :key="drive.drive_id"

                        >

                            <td>

                                {{ drive.job_title }}

                            </td>

                            <td>

                                <span
                                    v-if="drive.status === 'approved'"
                                    class="badge bg-success"
                                >
                                    Approved
                                </span>

                                <span
                                    v-else-if="drive.status === 'pending'"
                                    class="badge bg-warning"
                                >
                                    Pending
                                </span>

                                <span
                                    v-else-if="drive.status==='closed'"
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

                            <td>

                                {{ drive.applicant_count }}

                            </td>

                            <td>

                                {{ drive.application_deadline }}

                            </td>

                        </tr>

                        <tr v-if="companyDrives.length === 0">

                            <td colspan="5" class="text-center">

                                No Placement Drives Created

                            </td>

                        </tr>

                    </tbody>

                </table>

            </div>

        </div>

        <div v-if="activeSection==='company-profile'">

            <div class="card shadow">

                <div class="card-header">

                    <h3>

                        Company Profile

                    </h3>

                </div>

                <div class="card-body">

                    <div class="mb-3">

                        <label class="form-label">

                            Company Name

                        </label>

                        <input
                            class="form-control"
                            :value="dashboard.company_name"
                            disabled
                        >

                    </div>

                    <div class="mb-3">

                        <label class="form-label">

                            HR Contact

                        </label>

                        <input
                            class="form-control"
                            :value="dashboard.hr_contact_name"
                            disabled
                        >

                    </div>

                    <div class="mb-3">

                        <label class="form-label">

                            Website

                        </label>

                        <input
                            class="form-control"
                            :value="dashboard.website"
                            disabled
                        >

                    </div>

                    <div class="mb-3">

                        <label class="form-label">

                            Description

                        </label>

                        <textarea
                            class="form-control"
                            rows="4"
                            :value="dashboard.description"
                            disabled
                        ></textarea>

                    </div>

                    <div class="mb-3">

                        <label class="form-label">

                            Approval Status

                        </label>

                        <div>

                            <span
                                v-if="dashboard.approval_status==='approved'"
                                class="badge bg-success"
                            >
                                Approved
                            </span>

                            <span
                                v-else-if="dashboard.approval_status==='pending'"
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

                        </div>

                    </div>

                </div>

            </div>

        </div>

        <div v-if="activeSection === 'drives'">

            <div class="d-flex justify-content-between align-items-center mb-4">

                <h3>

                    Placement Drives

                </h3>

                <button

                    v-if="!showDriveForm"

                    class="btn btn-success"

                    @click="showDriveForm = true"

                >

                    <i class="bi bi-plus-circle me-2"></i>

                    Create New Drive

                </button>

            </div>

            <div v-if="showDriveForm">

                <div class="card shadow mb-4">

                    <div class="card-header">

                        <h5>

                            <i
                                :class="editingDrive ? 'bi bi-pencil-square me-2' : 'bi bi-plus-circle me-2'"
                            ></i>

                            {{ editingDrive ? "Edit Placement Drive" : "Create Placement Drive" }}

                        </h5>

                    </div>

                    <div class="card-body">

                        <div class="row">

                            <div class="col-md-6 mb-3">

                                <label class="form-label fw-bold">

                                    Job Title

                                </label>

                                <input
                                    type="text"
                                    class="form-control"
                                    v-model="newDrive.job_title"
                                >

                            </div>

                            <div class="col-md-6 mb-3">

                                <label class="form-label fw-bold">

                                    Graduation Year

                                </label>

                                <input
                                    type="number"
                                    class="form-control"
                                    v-model="newDrive.eligibility_year"
                                >

                            </div>

                        </div>

                        <div class="row">

                            <div class="col-md-6 mb-3">

                                <label class="form-label fw-bold">

                                    Minimum Required CGPA

                                </label>

                                <input
                                    type="number"
                                    step="0.01"
                                    class="form-control"
                                    v-model="newDrive.eligibility_cgpa"
                                >

                            </div>

                            <div class="col-md-6 mb-3">

                                <label class="form-label fw-bold">

                                    Application Deadline

                                </label>

                                <input
                                    type="date"
                                    class="form-control"
                                    v-model="newDrive.application_deadline"
                                >

                            </div>

                        </div>

                        <div class="mb-3">

                            <label class="form-label fw-bold">

                                Eligible Branches

                            </label>

                            <select
                                multiple
                                class="form-select"
                                v-model="newDrive.eligibility_branch"
                            >

                                <option>CSE</option>
                                <option>DS&AI</option>
                                <option>EE</option>
                                <option>EEE</option>
                                <option>ECE</option>
                                <option>ME</option>
                                <option>CE</option>

                            </select>

                            <small class="text-muted fw-semibold">

                                Hold Ctrl (Windows OS) or Cmd (Mac os) to select multiple branches.

                            </small>

                        </div>

                        <div class="mb-3">

                            <label class="form-label fw-bold">

                                Job Description

                            </label>

                            <textarea
                                rows="5"
                                class="form-control"
                                v-model="newDrive.job_description"
                            ></textarea>

                        </div>

                        <div class="d-flex justify-content-end gap-2">

                            <button

                                class="btn btn-secondary"

                                @click="cancelDriveForm"

                            >

                                Cancel

                            </button>

                            <button

                                class="btn btn-success"

                                @click="editingDrive ? updateDrive() : createDrive()"

                            >

                                {{ editingDrive ? "Save Changes" : "Create Drive" }}

                            </button>

                        </div>

                    </div>

                </div>

            </div>

        </div>

        <div v-if="activeSection === 'drives'">

            <hr class="my-4">

            <h3>

                My Placement Drives

            </h3>

            <table class="table table-bordered">

                <thead>

                    <tr>

                        <th>Job Title</th>

                        <th>Status</th>

                        <th>Deadline</th>

                        <th>Applicants</th>

                        <th>Actions</th>

                    </tr>

                </thead>

                <tbody>

                    <tr

                        v-for="drive in filteredCompanyDrives"

                        :key="drive.drive_id"

                    >

                        <td>

                            {{ drive.job_title }}

                        </td>

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

                        <td>

                            {{ drive.application_deadline }}

                        </td>

                        <td>

                            {{ drive.applicant_count }}

                        </td>

                        <td>

                            <button

                                class="btn btn-warning btn-sm me-2"

                                @click="editDrive(drive)"

                            >

                                <i class="bi bi-pencil-square"></i>

                                Edit

                            </button>

                            <button

                                v-if="drive.status === 'approved' || drive.status === 'closed'"

                                class="btn btn-secondary btn-sm"

                                @click="toggleDriveStatus(drive.drive_id)"

                            >

                                <i

                                    :class="drive.status === 'closed'
                                        ? 'bi bi-unlock-fill'
                                        : 'bi bi-lock-fill'"

                                ></i>

                                {{ drive.status === 'closed' ? 'Reopen' : 'Close' }}

                            </button>

                        </td>

                    </tr>

                    <tr v-if="companyDrives.length === 0">

                        <td colspan="5" class="text-center">

                            No Placement Drives Created

                        </td>

                    </tr>

                </tbody>

            </table>

        </div>

        <div v-if="activeSection === 'applicants'">


            <h3 class="mt-4">

                Applicants

            </h3>

            <div class="row mb-3">

                <div class="col-md-6">

                    <input
                        type="text"
                        class="form-control"
                        placeholder="Search by Student, Branch or Job Title"
                        v-model="applicationSearch"
                    >

                </div>

            </div>

            <table class="table table-bordered table-striped">

                <thead>

                    <tr>

                        <th>Name</th>
                        <th>Email</th>
                        <th>Job Title</th>
                        <th>Branch</th>
                        <th>CGPA</th>
                        <th>Status</th>
                        <th>Resume</th>
                        <th>Action</th>

                    </tr>

                </thead>

                <tbody>

                    <tr

                        v-for="application in filteredApplications"

                        :key="application.application_id"

                    >

                        <td>{{ application.student_name }}</td>

                        <td>{{ application.student_email }}</td>

                        <td>{{ application.job_title }}</td>

                        <td>{{ application.branch }}</td>

                        <td>{{ application.cgpa }}</td>

                        <td>

                            <span
                                v-if="application.application_status==='applied'"
                                class="badge bg-primary"
                            >
                                Applied
                            </span>

                            <span
                                v-else-if="application.application_status==='shortlisted'"
                                class="badge bg-warning text-dark"
                            >
                                Shortlisted
                            </span>

                            <span
                                v-else-if="application.application_status==='interview'"
                                class="badge bg-info text-dark"
                            >
                                Interview
                            </span>

                            <span
                                v-else-if="application.application_status==='selected'"
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

                            <a

                                :href="'http://127.0.0.1:5000/' + application.resume"

                                target="_blank"

                                class="btn btn-sm btn-primary"

                            >

                                Download

                            </a>

                        </td>

                        <td>

                            <template v-if="application.application_status === 'applied'">

                                <button
                                    class="btn btn-warning btn-sm me-2"
                                    @click="shortlist(application.application_id)"
                                >
                                    Shortlist
                                </button>

                                <button
                                    class="btn btn-danger btn-sm"
                                    @click="reject(application.application_id)"
                                >
                                    Reject
                                </button>

                            </template>

                            <template v-else-if="application.application_status === 'shortlisted'">

                                <button
                                    class="btn btn-primary btn-sm me-2"
                                    @click="interview(application.application_id)"
                                >
                                    Schedule Interview
                                </button>

                                <button
                                    class="btn btn-danger btn-sm"
                                    @click="reject(application.application_id)"
                                >
                                    Reject
                                </button>

                            </template>

                            <template v-else-if="application.application_status === 'interview'">

                                    <button
                                        class="btn btn-success btn-sm me-2"
                                        @click="select(application.application_id)"
                                    >
                                        Select
                                    </button>

                                    <button
                                        class="btn btn-danger btn-sm"
                                        @click="reject(application.application_id)"
                                    >
                                        Reject
                                    </button>

                                </template>

                            <template v-else-if="application.application_status === 'selected'">

                                <span class="badge bg-success">
                                    Selected
                                </span>

                            </template>

                            <template v-else-if="application.application_status === 'rejected'">

                                <span class="badge bg-danger">
                                    Rejected
                                </span>

                            </template>

                        </td>

                    </tr>

                    <tr v-if="filteredApplications.length === 0">

                        <td colspan="8" class="text-center text-muted">
                            
                            No applications yet.
                        
                        </td>

                    </tr>

                </tbody>

            </table>

        </div>

    </div>

</template>

<script setup>

import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import AppNavbar from "@/components/AppNavbar.vue"

const applications = ref([])
const companyDrives = ref([])
const newDrive = ref({

    job_title: "",

    job_description: "",

    eligibility_branch: [],

    eligibility_cgpa: "",

    eligibility_year: "",

    application_deadline: ""

})

const activeSection = ref("home")

const dashboard = ref({
    company_name: ""
})

const driveSearch = ref("")

const showDriveForm = ref(false)

const editingDrive = ref(null)

const applicationSearch = ref("")

onMounted(async () => {

    try {

        const dashboardResponse = await axios.get(

            "/company/dashboard",

            {
                withCredentials: true
            }

        )

        dashboard.value = dashboardResponse.data

        await loadCompanyDrives()

        await loadApplications()

    }

    catch (error) {

        console.log(error)

    }

})

const loadApplications = async () => {

    try {

        const response = await axios.get(

            "/company/applications",

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

const loadCompanyDrives = async () => {

    try {

        const response = await axios.get(

            "/company/drives",

            {
                withCredentials: true
            }

        )

        companyDrives.value = response.data

    }

    catch (error) {

        console.log(error)

    }

}

const shortlist = async (applicationId) => {

    try {

        const response = await axios.post(

            `/company/shortlist/${applicationId}`,

            {},

            {
                withCredentials: true
            }

        )

        alert(response.data.message)

        await loadApplications()

    }

    catch (error) {

        if (error.response) {

            alert(error.response.data.message)

        }

    }

}

const select = async (applicationId) => {

    try {

        const response = await axios.post(

            `/company/select/${applicationId}`,

            {},

            {
                withCredentials: true
            }

        )

        alert(response.data.message)

        await loadApplications()
    }

    catch (error) {

        if (error.response) {

            alert(error.response.data.message)

        }

    }

}

const reject = async (applicationId) => {

    try {

        const response = await axios.post(

            `/company/reject/${applicationId}`,

            {},

            {
                withCredentials: true
            }

        )

        alert(response.data.message)

        await loadApplications()

    }

    catch (error) {

        if (error.response) {

            alert(error.response.data.message)

        }

    }

}

const interview = async (applicationId) => {

    try {

        const response = await axios.post(

            `/company/interview/${applicationId}`,

            {},

            {
                withCredentials: true
            }

        )

        alert(response.data.message)

        await loadApplications()

    }

    catch (error) {

        if (error.response) {

            alert(error.response.data.message)

        }

    }

}

const createDrive = async () => {

    const formData = new FormData()

    formData.append(

        "job_title",

        newDrive.value.job_title

    )

    formData.append(

        "job_description",

        newDrive.value.job_description

    )

    newDrive.value.eligibility_branch.forEach(

        (branch) => {

            formData.append(

                "eligibility_branch",

                branch

            )

        }

    )

    formData.append(

        "eligibility_cgpa",

        newDrive.value.eligibility_cgpa

    )

    formData.append(

        "eligibility_year",

        newDrive.value.eligibility_year

    )

    formData.append(

        "application_deadline",

        newDrive.value.application_deadline

    )

    try {

        const response = await axios.post(

            "/company/create-drive",

            formData,

            {

                withCredentials: true

            }

        )

        alert(response.data.message)

        await loadCompanyDrives()

        cancelDriveForm()

        const dashboardResponse = await axios.get(

            "/company/dashboard",

            {
                withCredentials:true
            }

        )

        dashboard.value = dashboardResponse.data

    }

    catch (error) {

        if (error.response) {

            alert(error.response.data.message)

        }

    }

}

const updateDrive = async () => {

    const formData = new FormData()

    formData.append(

        "job_title",

        newDrive.value.job_title

    )

    formData.append(

        "job_description",

        newDrive.value.job_description

    )

    newDrive.value.eligibility_branch.forEach(

        (branch) => {

            formData.append(

                "eligibility_branch",

                branch

            )

        }

    )

    formData.append(

        "eligibility_cgpa",

        newDrive.value.eligibility_cgpa

    )

    formData.append(

        "eligibility_year",

        newDrive.value.eligibility_year

    )

    formData.append(

        "application_deadline",

        newDrive.value.application_deadline

    )

    try {

        const response = await axios.post(

            `/company/edit-drive/${editingDrive.value.drive_id}`,

            formData,

            {

                withCredentials: true

            }

        )

        alert(response.data.message)

        await loadCompanyDrives()

        cancelDriveForm()

        const dashboardResponse = await axios.get(

            "/company/dashboard",

            {
                withCredentials:true
            }

        )

        dashboard.value = dashboardResponse.data

    }

    catch (error) {

        if (error.response) {

            alert(error.response.data.message)

        }
    }
}

const toggleDriveStatus = async (driveId) => {

    try {

        const response = await axios.post(

            `/company/toggle-drive-status/${driveId}`,

            {},

            {

                withCredentials: true

            }

        )

        alert(response.data.message)

        await loadCompanyDrives()

        const dashboardResponse = await axios.get(

            "/company/dashboard",

            {

                withCredentials: true

            }

        )

        dashboard.value = dashboardResponse.data

    }

    catch (error) {

        if (error.response) {

            alert(error.response.data.message)

        }

        else {

            alert("Something went wrong.")

        }

    }

}

const editDrive = (drive) => {

    editingDrive.value = drive

    newDrive.value = {

        job_title: drive.job_title,

        job_description: drive.job_description,

        eligibility_branch: drive.eligibility_branch.split(","),

        eligibility_cgpa: drive.eligibility_cgpa,

        eligibility_year: drive.eligibility_year,

        application_deadline: drive.application_deadline

    }

    showDriveForm.value = true

}

const filteredCompanyDrives = computed(() => {

    return companyDrives.value.filter((drive) => {

        const search = driveSearch.value.toLowerCase()

        return (

            drive.job_title.toLowerCase().includes(search) ||

            drive.status.toLowerCase().includes(search)

        )

    })

})

const cancelDriveForm = () => {

    showDriveForm.value = false

    editingDrive.value = null

    newDrive.value = {

        job_title: "",

        job_description: "",

        eligibility_branch: [],

        eligibility_cgpa: "",

        eligibility_year: "",

        application_deadline: ""

    }

}

const filteredApplications = computed(() => {

    const search = applicationSearch.value.toLowerCase()

    return applications.value.filter((application) => {

        return (

            application.student_name.toLowerCase().includes(search) ||

            application.branch.toLowerCase().includes(search) ||

            application.job_title.toLowerCase().includes(search)

        )

    })

})
</script>

<style scoped>

.dashboard-card{

    cursor:pointer;

    transition:0.25s ease;

}

.dashboard-card:hover{

    transform:translateY(-5px);

    box-shadow:0px 8px 18px rgba(0,0,0,0.15);

}

</style>