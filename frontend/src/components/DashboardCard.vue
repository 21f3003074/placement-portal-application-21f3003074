<template>

    <div class="card shadow-sm border-0 rounded-4 mb-4">

        <div
            class="card-header bg-white border-0 py-3"
        >

            <h5
                class="mb-0 fw-bold text-primary"
            >

                <i
                    v-if="icon"
                    :class="icon"
                    class="me-2"
                ></i>

                {{ title }}

            </h5>

        </div>

        <div class="card-body">

            <slot></slot>

        </div>

    </div>

</template>

<script setup>

defineProps({

    title: String,

    icon: String

})

</script>

<style scoped>

.dashboard-card{

    cursor:pointer;

    transition:all .25s ease;

}

.dashboard-card:hover{

    transform:translateY(-6px);

    box-shadow:0 .75rem 1.5rem rgba(0,0,0,.18);

}

</style>