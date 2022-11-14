<script lang="ts">
import { defineComponent, ref } from 'vue'
import { NList, NListItem, NThing, NAvatar, NIcon } from 'naive-ui'
import { PersonFilled } from '@vicons/material'
const contacts = ref<any[]>([
    { name: 'John Doe', phone: '1234567890', email: 'test' },
    { name: 'John Doe', phone: '1234567890', email: 'test' },
    { name: 'John Doe', phone: '1234567890', email: 'test' },
])

export default defineComponent({
    name: 'Home',
    setup() {
        return {
            contacts
        }
    },
    props: {
        contacts: Array 
    },
    components: {
        NList,
        NListItem,
        NThing,
        NAvatar,
        NIcon,
        PersonFilled
    },
})
</script>


<template :contacts="contacts">
    <n-list>
        <n-list-item v-for="contact in contacts" :key="contact.name">
            <n-thing>
                <n-avatar>
                    <n-icon>
                        <person-filled />
                    </n-icon>
                </n-avatar>
                <span>{{ contact.name }}</span>
            </n-thing>
        </n-list-item>
    </n-list>
</template>