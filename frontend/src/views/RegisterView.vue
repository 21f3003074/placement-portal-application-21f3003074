<template>

    <div class="login-page">

        <div class="container py-5">

            <div class="row justify-content-center">

                <div class="col-lg-7 col-md-8">

                    <div class="card portal-card">

                        <div class="card-body p-4">

                            <div class="text-center mb-3">

                                <div class="display-5 text-primary mb-2">

                                    <i class="bi bi-mortarboard-fill"></i>

                                </div>

                                <h2 class="fw-bold mb-2">

                                    Create Account

                                </h2>

                                <p class="text-muted fw-bold mb-4">

                                    Placement Portal

                                </p>

                                <div class="d-grid gap-2 d-md-flex justify-content-center mb-4">

                                    <ul class="nav nav-pills nav-fill mb-4">

                                        <li class="nav-item">

                                            <button
                                                class="nav-link"
                                                :class="{ active: role==='student' }"
                                                @click="role='student'"
                                            >

                                                <i class="bi bi-person-fill me-2"></i>

                                                Student

                                            </button>

                                        </li>

                                        <li class="nav-item">

                                            <button
                                                class="nav-link"
                                                :class="{ active: role==='company' }"
                                                @click="role='company'"
                                            >

                                                <i class="bi bi-building me-2"></i>

                                                Company

                                            </button>

                                        </li>

                                    </ul>

                                </div>

                                <div v-if="role === 'student'">

                                        <div class="mb-3">

                                            <label class="form-label fw-semibold text-start d-block">

                                                Full Name

                                            </label>

                                            <div class ="input-group">
                                                
                                                <span class="input-group-text">

                                                    <i class="bi bi-person-fill"></i>

                                                </span>

                                                <input
                                                    v-model="student.name"
                                                    type="text"
                                                    class="form-control"
                                                    placeholder="Enter your full name"
                                                >

                                            </div>

                                        </div>

                                        <div class="mb-3">

                                            <label class="form-label fw-semibold text-start d-block">

                                                Email Address

                                            </label>

                                            <div class="input-group">
                                                
                                                <span class="input-group-text">

                                                    <i class="bi bi-envelope-fill"></i>

                                                </span>

                                                <input
                                                    v-model="student.email"
                                                    type="email"
                                                    class="form-control"
                                                    placeholder="name@example.com"
                                                >

                                            </div>

                                        </div>

                                        <div class="mb-3">

                                            <label class="form-label fw-semibold text-start d-block">

                                                Password

                                            </label>

                                            <div class="input-group">
                                                
                                                <span class="input-group-text">

                                                    <i class="bi bi-lock-fill"></i>

                                                </span>

                                                <input
                                                    v-model="student.password"
                                                    type="password"
                                                    class="form-control"
                                                    placeholder="Create a password"
                                                >

                                            </div>

                                        </div>

                                        <div class="row mb-3">

                                            <div class="col-md-4">

                                                <label class="form-label fw-semibold text-start d-block">

                                                    Branch

                                                </label>

                                                <div class="input-group">

                                                    <span class="input-group-text">

                                                        <i class="bi bi-diagram-3-fill"></i>

                                                    </span>

                                                    <select
                                                        class="form-select"
                                                        v-model="student.branch"
                                                    >

                                                        <option value="" disabled>
                                                            Select Branch
                                                        </option>

                                                        <option value="CSE">
                                                            CSE
                                                        </option>

                                                        <option value="DS&AI">
                                                            DS&AI
                                                        </option>

                                                        <option value="EE">
                                                            EE
                                                        </option>

                                                        <option value="EEE">
                                                            EEE
                                                        </option>

                                                        <option value="ECE">
                                                            ECE
                                                        </option>

                                                        <option value="ME">
                                                            ME
                                                        </option>

                                                        <option value="CE">
                                                            CE
                                                        </option>

                                                    </select>

                                                </div>

                                            </div>

                                            <div class="col-md-4">

                                                <label class="form-label fw-semibold text-start d-block">

                                                    CGPA

                                                </label>

                                                <div class="input-group">

                                                    <span class="input-group-text">

                                                        <i class="bi bi-award-fill"></i>

                                                    </span>

                                                    <input
                                                        type="number"
                                                        step="0.01"
                                                        min="0"
                                                        max="10"
                                                        class="form-control"
                                                        v-model="student.cgpa"
                                                        placeholder="0 - 10"
                                                    >

                                                </div>

                                            </div>

                                            <div class="col-md-4">

                                                <label class="form-label fw-semibold text-start d-block">

                                                    Graduation Year

                                                </label>

                                                <div class="input-group">

                                                    <span class="input-group-text">

                                                        <i class="bi bi-calendar-event-fill"></i>

                                                    </span>

                                                    <input
                                                        type="number"
                                                        class="form-control"
                                                        v-model="student.graduation_year"
                                                        placeholder="2027"
                                                    >

                                                </div>

                                            </div>

                                        </div>

                                        <button
                                            class="btn btn-primary w-100"
                                            @click="registerStudent"
                                        >

                                            <i class="bi bi-person-plus-fill me-2"></i>

                                            Register as Student

                                        </button>

                                    </div>

                                    <div v-if="role === 'company'">

                                        <div class="mb-3">

                                            <label class="form-label fw-semibold text-start d-block">

                                                Company Name

                                            </label>

                                            <div class="input-group">
                                                
                                                <span class="input-group-text">

                                                    <i class="bi bi-building"></i>

                                                </span>

                                                <input
                                                    v-model="company.company_name"
                                                    class="form-control"
                                                    placeholder="Enter your company name"
                                                >

                                            </div>

                                        </div>

                                        <div class="row">

                                            <div class="col-md-6 mb-3">

                                                <label class="form-label fw-semibold text-start d-block">

                                                Email

                                                </label>

                                                <div class="input-group" mb-3>
                                                    
                                                    <span class="input-group-text">

                                                        <i class="bi bi-envelope-fill"></i>

                                                    </span>

                                                    <input
                                                        v-model="company.email"
                                                        type="email"
                                                        class="form-control"
                                                        placeholder="name@example.com"
                                                    >

                                                </div>

                                            </div>

                                            <div class="col-md-6 mb-3">

                                                <label class="form-label fw-semibold text-start d-block">

                                                Password

                                                </label>

                                                <div class="input-group">
                                                    
                                                    <span class="input-group-text">

                                                        <i class="bi bi-lock-fill"></i>

                                                    </span>

                                                    <input
                                                        v-model="company.password"
                                                        type="password"
                                                        class="form-control"
                                                        placeholder="Create a password"
                                                    >

                                                </div>

                                            </div>

                                        </div>

                                        <div class="row">

                                            <div class="col-md-6 mb-3">

                                                <label class="form-label fw-semibold text-start d-block">

                                                HR Contact Name

                                                </label>

                                                <div class="input-group">

                                                    <span class="input-group-text">

                                                        <i class="bi bi-person-fill"></i>

                                                    </span>

                                                    <input
                                                        v-model="company.hr_contact_name"
                                                        class="form-control"
                                                        placeholder="Enter the HR's name"
                                                    >

                                                </div>

                                            </div>

                                            <div class="col-md-6 mb-3">

                                                <label class="form-label fw-semibold text-start d-block">

                                                Website URL

                                                </label>

                                                <div class="input-group">

                                                    <span class="input-group-text">

                                                        <i class="bi bi-globe"></i>

                                                    </span>

                                                    <input
                                                        v-model="company.website"
                                                        class="form-control"
                                                        placeholder="Enter your company's website URL"
                                                    >

                                                </div>

                                            </div>

                                        </div>

                                        <div class="mb-4">

                                            <label class="form-label fw-semibold text-start d-block">

                                                Description

                                            </label>

                                            <textarea
                                                v-model="company.description"
                                                rows="3"
                                                class="form-control"
                                                placeholder="Describe your company"
                                            ></textarea>

                                        </div>

                                        <button
                                            class="btn btn-success w-100"
                                            @click="registerCompany"
                                        >

                                            <i class="bi bi-building-add me-2"></i>

                                            Register Company

                                        </button>

                                    </div>

                            </div>

                            <hr>

                            <div class="text-center">

                                <p class="text-muted mb-2">

                                    Already have an account?

                                </p>

                                <router-link

                                    to="/"

                                    class="btn btn-outline-secondary"

                                >

                                    <i class="bi bi-box-arrow-in-left me-2"></i>

                                    Back to Login

                                </router-link>

                            </div>

                        </div>

                    </div>

                </div>

            </div>

        </div>

    </div>

</template>

<script setup>

import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()

import { useRoute } from 'vue-router'

const route = useRoute()

const role = ref(
    route.query.role || "student"
)

const student = ref({

    name: "",

    email: "",

    password: "",

    branch: "",

    cgpa: "",

    graduation_year: ""

})

const company = ref({

    company_name: "",

    hr_contact_name: "",

    email: "",

    password: "",

    website: "",

    description: ""

})

const registerStudent = async () => {

    if(!student.value.name || !student.value.email || !student.value.password || !student.value.branch || !student.value.cgpa || !student.value.graduation_year){

        alert("Please Fill All Fields")

        return

    }

    try {

        const formData = new FormData()

        formData.append("name", student.value.name)
        formData.append("email", student.value.email)
        formData.append("password", student.value.password)
        formData.append("branch", student.value.branch)
        formData.append("cgpa", student.value.cgpa)
        formData.append("graduation_year", student.value.graduation_year)

        const response = await axios.post(

            "/register",

            formData,

            {
                withCredentials: true
            }

        )

        alert(response.data.message)

        student.value = {

                name: "",

                email: "",

                password: ""

        }

        setTimeout(() => {

            router.push("/")

        }, 1000)

    }

    catch(error){

        if(error.response){

            alert(error.response.data.message)

        }

    }

}

const registerCompany = async () => {

    if(!company.value.company_name || !company.value.hr_contact_name || !company.value.email || !company.value.password || !company.value.description){

        alert("Please Fill All Fields")

        return

    }

    try{

        const formData = new FormData()

        formData.append("company_name", company.value.company_name)
        formData.append("hr_contact_name", company.value.hr_contact_name)
        formData.append("email", company.value.email)
        formData.append("password", company.value.password)
        formData.append("website", company.value.website)
        formData.append("description", company.value.description)

        const response = await axios.post(

            "/company-register",

            formData,

            {
                withCredentials: true
            }

        )

        alert(response.data.message)

            company.value = {

                company_name: "",

                hr_contact_name: "",

                email: "",

                password: "",

                website: "",

                description: ""

            }

        setTimeout(() => {

            router.push("/")

        }, 1000)

    }

    catch(error){

        if(error.response){

            alert(error.response.data.message)

        }

    }

}
</script>