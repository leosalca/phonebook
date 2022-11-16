<script lang="ts">
import { defineComponent, ref } from 'vue'
import { NList, NListItem, NThing, NAvatar, NIcon, NDivider, NSpace } from 'naive-ui'
import { PersonFilled, LocalPhoneFilled, AlternateEmailFilled, HouseFilled } from '@vicons/material'
import { useFetch } from '../store/store'

export default defineComponent({
    name: 'ContactList',
    setup() {
        const addContact = () => {
            
        }
        
        const { contacts, error } = useFetch('http://127.0.0.1:5000/getcontacts')
        
        return {
            contacts, addContact
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
    <n-list clickable v-for="contact in contacts" class="contactList">
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
                    {{ contact?.company?.name }}
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
                        {{ contact?.address?.street }}
                        {{ contact?.address?.city }}
                        {{ contact?.address?.state }}
                        {{ contact?.address?.zipcode }}
                    </n-space>
            </n-thing>
        </n-list-item>
    </n-list>
</template>