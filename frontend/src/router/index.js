import { createRouter, createWebHashHistory } from 'vue-router'

import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import AdminDashboard from '../views/AdminDashboard.vue'
import StudentDashboard from '../views/StudentDashboard.vue'
import CompanyDashboard from '../views/CompanyDashboard.vue'

const router = createRouter({

    history: createWebHashHistory(),

    routes: [

        {
            path: '/',
            name: 'login',
            component: LoginView
        },

        {
            path: "/register",
            name: "register",
            component: RegisterView
        },

        {
            path: '/admin-dashboard',
            name: 'admin-dashboard',
            component: AdminDashboard
        },

        {
            path: '/student-dashboard',
            name: 'student-dashboard',
            component: StudentDashboard
        },

        {
            path: '/company-dashboard',
            name: 'company-dashboard',
            component: CompanyDashboard
        }

    ]

})

export default router