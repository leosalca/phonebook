<script lang="ts">
import { defineComponent, ref } from 'vue'
import { NList, NListItem, NThing, NAvatar, NIcon, NDivider, NSpace } from 'naive-ui'
import { PersonFilled, LocalPhoneFilled, AlternateEmailFilled, HouseFilled } from '@vicons/material'
import Contact from '../types/Contact'
import { useFetch } from '../store/store'

const { data, error } = useFetch('https://jsonplaceholder.typicode.com/users')


const contacts = data

export default defineComponent({
    name: 'ContactList',
    setup() {
        const addContact = () => {
            
        }

        const addedContacts = ref<[]>([]);

        return {
            contacts, addContact, addedContacts
        }
    },
    props: {
        contacts: Array,
        addedContacts: Array
    },
    components: {
        NList,
        NListItem,
        NThing,
        NAvatar,
        NIcon,
        NDivider,
        NSpace,
        PersonFilled,
        LocalPhoneFilled,
        AlternateEmailFilled,
        HouseFilled
    }
})
</script>


<template :contacts="contacts" :addedContacts="addedContacts">
    <n-list clickable v-for="contact in contacts">
        <n-list-item :key="contact.name">
            <n-thing content-intended class="contactItem">
                <template #avatar>
                    <n-avatar>
                        <n-icon>
                            <person-filled />
                        </n-icon>
                    </n-avatar>
                </template>
                <template #header>
                    {{ contact.name }}
                </template>
                <template #description>
                    Description
                </template>
                <n-divider />
                    <n-space>
                        <n-icon>
                            <local-phone-filled />
                        </n-icon>
                        {{ contact.phone }}
                    </n-space>
                    <n-space>
                        <n-icon>
                            <alternate-email-filled />
                        </n-icon>
                        {{ contact.email }}
                    </n-space>
                    <n-space>
                        <n-icon>
                            <house-filled />
                        </n-icon>
                        {{ contact.address }}
                    </n-space>
            </n-thing>
        </n-list-item>
    </n-list>
</template>