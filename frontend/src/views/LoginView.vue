<template>
  <div class="login-page">

    <div class="container py-5">

      <div class="row justify-content-center">

        <div class="col-md-5">

          <div class="card shadow-lg border-0 rounded-4 login-card">

            <div class="text-center mb-2">

              <div
                  class="display-5 text-primary mb-2"
              >

                  <i class="bi bi-mortarboard-fill"></i>

              </div>

              <h2
                  class="fw-bold mb-2"
              >

                  Placement Portal

              </h2>

              <p class="text-muted fw-bold mb-2">

                  Training & Placement Cell

              </p>

              <!-- <p class="text-secondary small mb-4">

                  Training & Placement Cell

              </p> -->

          </div>

            <div class="card-body pt-3 pb-4 px-4">

              <h5 class="text-center mb-3">

                  Login to Continue

              </h5>

              <div class="mb-2">
                <label class="form-label">
                  Email
                </label>

                <div class="input-group mb-3">

                    <span class="input-group-text">

                        <i class="bi bi-envelope-fill"></i>

                    </span>

                    <input

                        type="email"

                        class="form-control"

                        placeholder="name@example.com"

                        v-model="email"

                    >

                </div>

              </div>

              <div class="mb-2">
                <label class="form-label">
                  Password
                </label>

                <div class="input-group mb-4">

                    <span class="input-group-text">

                        <i class="bi bi-lock-fill"></i>

                    </span>

                    <input

                        type="password"

                        class="form-control"

                        placeholder="Enter your password"

                        v-model="password"

                    >

                </div>

              </div>

              <button

                  class="btn btn-primary w-100 py-2"

                  @click="login"

              >

                  <i class="bi bi-box-arrow-in-right me-2"></i>

                  Login

              </button>

              <hr>

              <div class="text-center">

                  <p class="mb-2">

                      New User?

                  </p>

                  <router-link

                      to="/register?role=student"

                      class="btn btn-outline-primary btn-sm me-2"

                  >

                      <i class="bi bi-person-fill me-1"></i>

                      Register as Student

                  </router-link>

                  <router-link

                      to="/register?role=company"

                      class="btn btn-outline-success btn-sm"

                  >

                      <i class="bi bi-building me-1"></i>

                      Register as Company

                  </router-link>

                  <hr>

                  <p class="text-center text-muted small mb-0">

                      © 2026 Placement Portal

                  </p>

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
import { useRouter } from 'vue-router'
import axios from 'axios'

const email = ref('')
const password = ref('')
const router = useRouter()

const login = async () => {

    try {

        const response = await axios.post(
            "/login",
            {
                email: email.value,
                password: password.value
            },
            {
                withCredentials: true
            }
        )

        console.log(response.data)

        if (response.data.role === "admin") {

          router.push("/admin-dashboard")

        } else if (response.data.role === "company") {

          router.push("/company-dashboard")

        } else if (response.data.role === "student") {
          
          router.push("/student-dashboard")
        }

    }

    catch (error) {

        console.log(error)

    }

}

</script>