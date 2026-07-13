<template>

    <AppNavbar

        role="student"

        :username="profile.name"

        :activeSection="activeSection"

        @change-section="activeSection = $event"

    />

    <div class="container pt-5" style="margin-top: 20px;">

        <DashboardCard

            v-if="activeSection === 'home'"

            title="Dashboard Overview"

            icon="bi bi-speedometer2"

        >

            <h2 class="fw-bold mb-2">

                Welcome Back, {{ profile.name }}

            </h2>

            <p class="text-muted mb-4">

                Here's a quick overview of your placement activities.

            </p>

            <div class="row g-4">

                <div class="col-md-3">

                    <div class="card border-0 shadow-sm text-center h-100 dashboard-card"
                        @click="activeSection='drives'"
                    >

                        <div class="card-body">

                            <i
                                class="bi bi-briefcase-fill text-primary fs-1"
                            ></i>

                            <h5 class="mt-3">

                                Available Drives

                            </h5>

                            <h2 class="fw-bold">

                                {{ filteredDrives.length }}

                            </h2>

                        </div>

                    </div>

                </div>

                <div class="col-md-3">

                    <div class="card border-0 shadow-sm text-center h-100 dashboard-card"
                        @click="activeSection='applications'"
                    >

                        <div class="card-body">

                            <i
                                class="bi bi-file-earmark-check-fill text-success fs-1"
                            ></i>

                            <h5 class="mt-3">

                                Applications

                            </h5>

                            <h2 class="fw-bold">

                                {{ applications.length }}

                            </h2>

                        </div>

                    </div>

                </div>

                <div class="col-md-3">

                    <div class="card border-0 shadow-sm text-center h-100 dashboard-card"
                        @click="activeSection='profile'"
                    >

                        <div class="card-body">

                            <i
                                class="bi bi-person-badge-fill text-warning fs-1"
                            ></i>

                            <h5 class="mt-3">

                                Profile

                            </h5>

                            <h5

                                class="fw-bold"

                                :class="profileComplete ? 'text-success' : 'text-danger'"

                            >

                                {{ profileComplete ? "Complete" : "Incomplete" }}

                            </h5>

                        </div>

                    </div>

                </div>

                <div class="col-md-3">

                    <div class="card border-0 shadow-sm text-center h-100 dashboard-card"
                        @click="activeSection='profile'"
                    >

                        <div class="card-body">

                            <i
                                class="bi bi-file-earmark-arrow-up-fill text-danger fs-1"
                            ></i>

                            <h5 class="mt-3">

                                Resume

                            </h5>

                            <h5

                                class="fw-bold"

                                :class="profile.resume ? 'text-success' : 'text-danger'"

                            >

                                {{ profile.resume ? "Uploaded" : "Not Uploaded" }}

                            </h5>

                        </div>

                    </div>

                </div>

            </div>

            <hr class="my-5">

            <h4 class="fw-bold mb-3">

                Recent Placement Drives

            </h4>

            <div class="table-responsive">

                <table class="table table-hover align-middle">

                    <thead class="table-light">

                        <tr>

                            <th>Job Title</th>

                            <th>Branch</th>

                            <th>CGPA</th>

                            <th>Deadline</th>

                        </tr>

                    </thead>

                    <tbody>

                        <tr

                            v-for="drive in filteredDrives.slice(0,5)"

                            :key="drive.id"

                        >

                            <td>

                                {{ drive.job_title }}

                            </td>

                            <td>

                                {{ drive.eligibility_branch }}

                            </td>

                            <td>

                                {{ drive.eligibility_cgpa }}

                            </td>

                            <td>

                                {{ drive.application_deadline }}

                            </td>

                        </tr>

                        <tr v-if="filteredDrives.length===0">

                            <td colspan="4" class="text-center">

                                No Placement Drives Available

                            </td>

                        </tr>

                    </tbody>

                </table>

            </div>

        </DashboardCard>

        <DashboardCard

            v-if="activeSection === 'profile'"

            title="My Profile"

            icon="bi bi-person-circle"

        >

            <div class="row">

                <div class="col-md-6 mb-3">

                    <label class="form-label">

                        Name

                    </label>

                    <input

                        type="text"

                        class="form-control"

                        :value="profile.name"

                        disabled

                    >

                </div>

                <div class="col-md-6 mb-3">

                    <label class="form-label">

                        Email

                    </label>

                    <input

                        type="email"

                        class="form-control"

                        :value="profile.email"

                        disabled

                    >

                </div>

            </div>

            <div class="row">

                <div class="col-md-6 mb-3">

                    <label class="form-label">

                        Branch

                    </label>

                    <input

                        type="text"

                        class="form-control"

                        :value="profile.branch"

                        disabled

                    >

                </div>

                <div class="col-md-6 mb-3">

                    <label class="form-label">

                        CGPA

                    </label>

                    <input

                        type="number"

                        step="0.01"

                        class="form-control"

                        v-model="profile.cgpa"

                    >

                </div>

            </div>

            <div class="row">

                <div class="col-md-6 mb-3">

                    <label class="form-label">

                        Graduation Year

                    </label>

                    <input

                        type="number"

                        class="form-control"

                        :value="profile.graduation_year"

                        disabled

                    >

                </div>

                <div class="col-md-6 mb-3">

                    <label class="form-label">

                        Resume

                    </label>

                    <input

                        type="file"

                        class="form-control"

                        @change="selectResume"

                    >

                </div>

            </div>

            <div class="text-center mt-4">

                <button

                    class="btn btn-primary px-5"

                    @click="saveProfile"

                >

                    <i class="bi bi-floppy-fill me-2"></i>

                    Save Profile

                </button>

            </div>

        </DashboardCard>

        <DashboardCard

            v-if="activeSection === 'drives'"

            title="Available Placement Drives"

            icon="bi bi-briefcase-fill"

        >

            <hr>

                <div class="mb-3">

                    <input

                        type="text"

                        class="form-control"

                        placeholder="Search by Job Title or Company or Branch"

                        v-model="driveSearch"

                    >

                </div>

                <table class="table table-bordered mt-3">

                    <thead class="table-light">

                        <tr>

                            <th>Job Title</th>

                            <th>Company</th>

                            <th>Eligibility</th>

                            <th>Deadline</th>

                            <th>Status</th>

                            <th>Action</th>

                        </tr>

                    </thead>

                    <tbody>

                        <tr
                            v-for="drive in filteredDrives"
                            :key="drive.id"
                        >

                            <td>

                                <strong>{{ drive.job_title }}</strong>

                            </td>

                            <td>

                                {{ drive.company_name }}

                            </td>

                            <td>

                                {{ drive.eligibility_branch }}

                                <br>

                                <small class="text-muted">

                                    CGPA ≥ {{ drive.eligibility_cgpa }}

                                </small>

                                <br>

                                <small class="text-muted">

                                    {{ drive.eligibility_year }} Batch

                                </small>

                            </td>

                            <td>

                                {{ drive.application_deadline }}

                            </td>

                            <td>

                                <span
                                    v-if="drive.already_applied"
                                    class="badge bg-primary"
                                >
                                    Applied
                                </span>

                                <span
                                    v-else-if="drive.eligible"
                                    class="badge bg-success"
                                >
                                    Eligible
                                </span>

                                <span
                                    v-else
                                    class="badge bg-danger"
                                >
                                    Not Eligible
                                </span>

                            </td>

                            <td>

                                <button
                                    v-if="drive.already_applied"
                                    class="btn btn-secondary btn-sm"
                                    disabled
                                >
                                    Applied
                                </button>

                                 <button
                                    v-else-if="drive.is_deadline_over"
                                    class="btn btn-danger btn-sm"
                                    disabled
                                >
                                    Deadline Over
                                </button>

                                <button
                                    v-else-if="drive.eligible"
                                    class="btn btn-success btn-sm"
                                    @click="applyDrive(drive.id)"
                                >
                                    Apply
                                </button>

                                <button
                                    v-else
                                    class="btn btn-secondary btn-sm"
                                    disabled
                                >
                                    Not Eligible
                                </button>

                            </td>

                        </tr>

                        <tr v-if="filteredDrives.length === 0">

                            <td colspan="6" class="text-center">

                                No Placement Drive Found.

                            </td>

                        </tr>

                    </tbody>

                </table>

                <hr>

        </DashboardCard>

        <DashboardCard

            v-if="activeSection === 'applications'"

            title="My Applications"

            icon="bi bi-file-earmark-text-fill"

        >

            <div class="row mb-4">

                <div class="col-md-3">

                    <div class="card shadow-sm border-0 text-center">

                        <div class="card-body">

                            <i class="bi bi-file-earmark-text fs-2 text-primary"></i>

                            <h6 class="mt-2">
                                Total
                            </h6>

                            <h3>
                                {{ applications.length }}
                            </h3>

                        </div>

                    </div>

                </div>

                <div class="col-md-3">

                    <div class="card shadow-sm border-0 text-center">

                        <div class="card-body">

                            <i class="bi bi-hourglass-split fs-2 text-warning"></i>

                            <h6 class="mt-2">
                                Applied
                            </h6>

                            <h3>
                                {{ appliedCount }}
                            </h3>

                        </div>

                    </div>

                </div>

                <div class="col-md-3">

                    <div class="card shadow-sm border-0 text-center">

                        <div class="card-body">

                            <i class="bi bi-check-circle fs-2 text-primary"></i>

                            <h6 class="mt-2">
                                Shortlisted
                            </h6>

                            <h3>
                                {{ shortlistedCount }}
                            </h3>

                        </div>

                    </div>

                </div>

                <div class="col-md-3">

                    <div class="card shadow-sm border-0 text-center">

                        <div class="card-body">

                            <i class="bi bi-trophy fs-2 text-success"></i>

                            <h6 class="mt-2">
                                Selected
                            </h6>

                            <h3>
                                {{ selectedCount }}
                            </h3>

                        </div>

                    </div>

                </div>

            </div>

                <table class="table table-bordered table-striped">

                    <thead>

                        <tr>

                            <th>Company</th>
                            <th>Job Title</th>
                            <th>Applied On</th>
                            <th>Status</th>

                        </tr>

                    </thead>

                    <tbody>

                        <tr
                            v-for="application in applications"
                            :key="application.application_id"
                        >

                            <td>
                                {{ application.company_name }}
                            </td>

                            <td>
                                {{ application.job_title }}
                            </td>

                            <td>
                                {{ application.application_date }}
                            </td>

                            <td>
                                <span
                                    v-if="application.status === 'applied'"
                                    class="badge bg-warning text-dark"
                                >
                                    Applied
                                </span>

                                <span
                                    v-else-if="application.status === 'shortlisted'"
                                    class="badge bg-primary"
                                >
                                    Shortlisted
                                </span>

                                <span
                                    v-else-if="application.status === 'selected'"
                                    class="badge bg-success"
                                >
                                    Selected
                                </span>

                                <span
                                    v-else-if="application.status === 'rejected'"
                                    class="badge bg-danger"
                                >
                                    Rejected
                                </span>

                                <span
                                    v-else
                                    class="badge bg-secondary"
                                >
                                    {{ application.status }}
                                </span>
                            </td>

                        </tr>

                        <tr v-if="applications.length === 0">

                            <td colspan="4" class="text-center text-muted">

                                You have not applied to any drives yet.

                            </td>

                        </tr>

                    </tbody>

                </table>


        </DashboardCard>

        <DashboardCard

            v-if="activeSection === 'exports'"

            title="Export Applications"

            icon="bi bi-download"

        >

                <button
                    class="btn btn-primary"
                    @click="exportApplications"
                >
                    Export CSV
                </button>

                <table class="table table-bordered mt-3">

                    <thead>

                        <tr>

                            <th>Job ID</th>
                            <th>Status</th>
                            <th>Download</th>

                        </tr>

                    </thead>

                    <tbody>

                        <tr
                            v-for="job in exportJobs"
                            :key="job.job_id"
                        >

                            <td>
                                {{ job.job_id }}
                            </td>

                            <td>
                                {{ job.status }}
                            </td>

                            <td>

                                <a
                                    v-if="job.status === 'completed'"
                                    :href="'http://127.0.0.1:5000/exports/' + job.filename"
                                    target="_blank"
                                    class="btn btn-success btn-sm"
                                >
                                    Download
                                </a>

                                <span v-else>

                                    Processing...

                                </span>

                            </td>

                        </tr>

                    </tbody>

                </table>

        </DashboardCard>

    </div>

</template>

<script setup>
import AppNavbar from "@/components/AppNavbar.vue"
import DashboardCard from "@/components/DashboardCard.vue"
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'

const activeSection = ref("home")
const profile = ref({})
const resume = ref(null)
const drives = ref([])
const applications = ref([])
const driveSearch = ref("")
const exportJobs = ref([])
let pollingInterval = null


onMounted(async () => {

    try {

        const response = await axios.get(

            "/student/profile",

            {
                withCredentials: true
            }

        )

        profile.value = response.data

        const drivesResponse = await axios.get(

            "/student/drives",

            {
                withCredentials: true
            }

        )

        drives.value = drivesResponse.data

        console.log(profile.value)
        console.log("Drives:", JSON.stringify(drives.value, null, 2))

        const applicationsResponse = await axios.get(

            "/student/applications",

            {
                withCredentials: true
            }

        )

        applications.value = applicationsResponse.data

        await loadExportJobs()

        console.log(applications.value)

        const processingJobs = exportJobs.value.filter(

            (job) =>

                job.status === "pending" ||

                job.status === "processing"

        )

        if (processingJobs.length > 0) {

            pollExportJobs()

        }

    }

    catch (error) {

        console.log(error)

    }

})

const selectResume = (event) => {

    resume.value = event.target.files[0]

    console.log(resume.value)

}

const saveProfile = async () => {

    console.log("Save Button Clicked")

    const formData = new FormData()

    formData.append(
        "branch",
        profile.value.branch
    )

    formData.append(
        "cgpa",
        profile.value.cgpa
    )

    formData.append(
        "graduation_year",
        profile.value.graduation_year
    )

    if (resume.value) {

        formData.append(
            "resume",
            resume.value
        )
    }

    try {

        await axios.post(

            "/student/profile",

            formData,

            {
                withCredentials: true
            }

        )

        alert("Profile Saved Successfully")

    }

    catch (error) {

        console.log(error)

        alert("Unable to Save Profile")

    }

}

const applyDrive = async (driveId) => {

    try {

        const response = await axios.post(

            `/apply/${driveId}`,

            {},

            {
                withCredentials: true
            }

        )

        alert(response.data.message)

    }

    catch (error) {

        if (error.response) {

            alert(error.response.data.message)

        } else {

            console.log(error)

        }

    }

}

const filteredDrives = computed(() => {

    if (driveSearch.value === "") {

        return drives.value

    }

    return drives.value.filter((drive) => {

        const search = driveSearch.value.toLowerCase()

        return (

            drive.job_title
                .toLowerCase()
                .includes(search)

            ||

            drive.eligibility_branch
                .toLowerCase()
                .includes(search)

            ||

            drive.company_name
                .toLowerCase()
                .includes(search)


        )

    })
})

const loadExportJobs = async () => {

    try {

        const response = await axios.get(

            "/student/exports",

            {
                withCredentials: true
            }

        )

        exportJobs.value = response.data

    }

    catch (error) {

        console.log(error)

    }

}

const pollExportJobs = () => {

    if (pollingInterval) {

        return

    }

    pollingInterval = setInterval(

        async () => {

            await loadExportJobs()

            const processingJobs = exportJobs.value.filter(

                (job) =>

                    job.status === "pending" ||

                    job.status === "processing"

            )

            if (processingJobs.length === 0) {

                clearInterval(pollingInterval)

                pollingInterval = null

            }

        },

        2000

    )

}

const exportApplications = async () => {

    try {

        const response = await axios.get(

            "/student/export",

            {
                withCredentials: true
            }

        )

        alert(response.data.message)

        await loadExportJobs()

        pollExportJobs()

    }

    catch (error) {

        if (error.response) {

            alert(error.response.data.message)

        }

    }

}

const profileComplete = computed(() => {

    return (

        profile.value.branch &&

        profile.value.cgpa &&

        profile.value.graduation_year &&

        profile.value.resume

    )

})

const appliedCount = computed(() => {

    return applications.value.filter(

        application => application.status === "applied"

    ).length

})

const shortlistedCount = computed(() => {

    return applications.value.filter(

        application => application.status === "shortlisted"

    ).length

})

const selectedCount = computed(() => {

    return applications.value.filter(

        application => application.status === "selected"

    ).length

})
</script>

<style scoped>

.dashboard-card{

    cursor:pointer;

    transition:0.25s;

}

.dashboard-card:hover{

    transform:translateY(-5px);

}

</style>