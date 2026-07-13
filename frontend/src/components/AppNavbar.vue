<template>

    <nav class="navbar navbar-expand-lg navbar-dark bg-primary shadow-sm">

        <div class="container-fluid">

            <router-link
                class="navbar-brand fw-bold"
                to="/"
            >

                <i class="bi bi-mortarboard-fill me-2"></i>

                Placement Portal

            </router-link>

            <button
                class="navbar-toggler"
                type="button"
                data-bs-toggle="collapse"
                data-bs-target="#navbarContent"
            >

                <span class="navbar-toggler-icon"></span>

            </button>

            <div
                class="collapse navbar-collapse"
                id="navbarContent"
            >

                <ul class="navbar-nav me-auto">

                    <li class="nav-item">

                        <a href="#" class="nav-link" :class="{active: activeSection === 'home'}" @click.prevent="$emit('change-section','home')">
                            Home
                        </a>

                    </li>

                    <template v-if="role==='student'">

                        <li class="nav-item">

                            <a href="#" class="nav-link" :class="{active: activeSection === 'profile'}" @click.prevent="$emit('change-section','profile')">

                                Profile

                            </a>

                        </li>

                        <li class="nav-item">

                            <a href="#" class="nav-link" :class="{active: activeSection === 'drives'}" @click.prevent="$emit('change-section','drives')">

                                Drives

                            </a>

                        </li>

                        <li class="nav-item">

                            <a href="#" class="nav-link" :class="{active: activeSection === 'applications'}" @click.prevent="$emit('change-section','applications')">

                                Applications

                            </a>

                        </li>

                        <li class="nav-item">

                            <a href="#" class="nav-link" :class="{active: activeSection === 'exports'}" @click.prevent="$emit('change-section','exports')">

                                Exports

                            </a>

                        </li>

                    </template>

                    <template v-else-if="role==='company'">

                        <li class="nav-item">

                            <a class="nav-link" href="#" :class="{active: activeSection === 'company-profile'}" @click.prevent="$emit('change-section','company-profile')">

                                Company Profile

                            </a>

                        </li>

                        <li class="nav-item">

                            <a href="#" class="nav-link" :class="{active: activeSection === 'drives'}" @click.prevent="$emit('change-section','drives')">

                                Drives

                            </a>

                        </li>

                        <li class="nav-item">

                            <a href="#" class="nav-link" :class="{active: activeSection === 'applicants'}" @click.prevent="$emit('change-section','applicants')">

                                Applicants

                            </a>

                        </li>

                    </template>

                    <template v-else>

                        <li class="nav-item">

                            <a href="#" class="nav-link" :class="{active: activeSection === 'students'}" @click.prevent="$emit('change-section','students')">

                                Students

                            </a>

                        </li>

                        <li class="nav-item">

                            <a href="#" class="nav-link" :class="{active: activeSection === 'companies'}" @click.prevent="$emit('change-section','companies')">

                                Companies

                            </a>

                        </li>

                        <li class="nav-item">

                            <a href="#" class="nav-link" :class="{active: activeSection === 'drives'}" @click.prevent="$emit('change-section','drives')">

                                Drives

                            </a>

                        </li>

                        <li class="nav-item">

                            <a href="#" class="nav-link" :class="{active: activeSection === 'applications'}" @click.prevent="$emit('change-section','applications')">

                                Applications

                            </a>

                        </li>

                    </template>

                </ul>
                <span class="navbar-text text-white me-3">

                    <i class="bi bi-person-circle me-2"></i>
                    Welcome, {{ username }}

                </span>

                <button
                    class="btn btn-outline-light btn-sm"
                    @click="logout"
                >

                    <i class="bi bi-box-arrow-right me-1"></i>

                    Logout

                </button>

            </div>

        </div>

    </nav>

</template>

<script setup>

import axios from 'axios'
import { useRouter } from 'vue-router'

defineProps({

    username:{

        type:String,

        default:"User"

    },

    role:{

        type:String,

        default:"student"

    },

    activeSection:{

        type:String,

        default:"home"

    }

})

const router = useRouter()

const logout = async () => {

    try {

        await axios.post(

            "/logout",

            {},

            {

                withCredentials: true

            }

        )

    }

    catch (error) {

        console.log(error)

    }

    router.push("/")

}

</script>

<style scoped>

.nav-link.active{

    color:white !important;

    font-weight:700;

    border-bottom:3px solid white;

}

</style>