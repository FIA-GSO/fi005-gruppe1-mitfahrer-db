<script setup lang="ts">
import { useRouter } from 'vue-router';

const router = useRouter();

defineProps({
    title: String,
    message: String
})
</script>

<template>
    <div class="bg-white dark:text-white grow w-screen flex items-center justify-center">
        <div
            class="container xs:rounded-none sm:rounded sm:max-w-md xs:w-screen w-md center sm:border-2 sm:border-gray-400 p-8 pb-4 flex flex-col align-center">
            <h1 class="text-3xl mb-4">
                <font-awesome-icon icon="fa-solid fa-dumpster-fire" class="text-red-400" /> {{ title }}
            </h1>
            <p class="mb-8">{{ message }}</p>
            <FormKit type="button" label="Zur Startseite" @click="router.push({ name: 'home' })"></FormKit>
        </div>
    </div>
</template>