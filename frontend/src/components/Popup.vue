<script setup lang="ts">
import { ref } from 'vue';


var isShown = ref(true)

function showPopup() {
    isShown.value = true
}

function hidePopup() {
    console.log("Hiding")
    isShown.value = false
    console.log(isShown)
} 

function togglePopup() {
    isShown.value != isShown.value
}

defineExpose({
    showPopup,
    hidePopup
})

</script>

<template>
    <div v-if="isShown" v-on:click="hidePopup" class="fixed top-0 left-0 w-full h-full z-40 bg-backdrop cursor-pointer"></div>
    <div v-if="isShown" class="fixed z-50" :style="{top: 0, right: 0}">
        <slot></slot>
    </div>
    
</template>

<style scoped>
:slotted(*) {
    @apply z-50;
}
</style>