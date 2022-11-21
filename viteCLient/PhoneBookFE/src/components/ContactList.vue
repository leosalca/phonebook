<script lang="ts">
import { defineComponent, ref } from 'vue'
import { NList, NListItem, NThing, NAvatar, NIcon, NDivider, NSpace } from 'naive-ui'
import { PersonFilled, LocalPhoneFilled, AlternateEmailFilled, HouseFilled } from '@vicons/material'
import { Contact } from '../types/contact'
import { useFetchContacts } from '../composables/useFetchContacts'
import { useContactStore } from '../stores/useContactStore'

export default defineComponent({
    name: 'ContactList',
    setup() {

        const store = useContactStore()

        fetch('http://127.0.0.1:5000/getcontacts')
            .then(res => res.json())
            .then(data => {
                store.setContacts(data)
                console.log(data)
            })
        
        return {
            store
        }
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

<template>
    <n-list  clickable class="contactList">
        <n-list-item key="listID++" clickable v-for="contact in store.contacts">
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
                    {{ contact?.company }}
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