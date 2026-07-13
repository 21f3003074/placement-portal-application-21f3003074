import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

export default defineConfig({

  plugins: [

    vue(),
    vueDevTools()

  ],

  resolve: {

    alias: {

      '@': fileURLToPath(
        new URL('./src', import.meta.url)
      ),

    },

  },

  server: {
  proxy: {
    "/login": {
      target: "http://127.0.0.1:5000",
      changeOrigin: true
    },
    "/register": {
      target: "http://127.0.0.1:5000",
      changeOrigin: true
    },
    "/logout": {
      target: "http://127.0.0.1:5000",
      changeOrigin: true
    },
    "/student": {
      target: "http://127.0.0.1:5000",
      changeOrigin: true
    },
    "/admin": {
      target: "http://127.0.0.1:5000",
      changeOrigin: true
    },
    "/company": {
      target: "http://127.0.0.1:5000",
      changeOrigin: true
    },
    "/company_profile": {
      target: "http://127.0.0.1:5000",
      changeOrigin: true
    },
    "/apply": {
      target: "http://127.0.0.1:5000",
      changeOrigin: true
    }
  }
}

})