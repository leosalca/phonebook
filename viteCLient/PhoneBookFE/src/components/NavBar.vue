<script lang="ts">
import { defineComponent, ref } from 'vue'
import { PersonAddSharp } from '@vicons/material'
import { NButton, NIcon } from 'naive-ui'
import {  useRouter } from 'vue-router'


export default defineComponent({
    name: 'NavBar',
    setup() {
        const router = useRouter()
        const handleAddContact = async () => {
            await router.push('/add')

        }
        return {
            handleAddContact 
        }
    },
    components: {
        NButton,
        NIcon,
        PersonAddSharp
    }
})

</script>
<template>
    <nav class="navigation">
        <router-link to="/">Contacts</router-link>
        <n-button class="addButton" circle ghost @click="handleAddContact()" >
            <template #icon>
                <n-icon><PersonAddSharp/></n-icon>
            </template>
        </n-button>
    </nav>
</template>
