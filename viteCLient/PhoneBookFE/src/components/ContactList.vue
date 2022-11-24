<script lang="ts">
import { defineComponent, ref } from 'vue';
import { NList, NListItem, NThing, NAvatar, NIcon, NDivider, NSpace, NButton } from 'naive-ui';
import { PersonFilled, LocalPhoneFilled, AlternateEmailFilled, HouseFilled, DeleteFilled } from '@vicons/material';
import { useContactStore } from '../stores/useContactStore';
import type { Contact } from '../types/contact';
import { useRouter } from 'vue-router';

export default defineComponent({
    name: 'ContactList',
    setup() {

        // define router and store to navigate to different routes and access states and actions from store
        const store = useContactStore();
        const router = useRouter();

        // function to delete contact. User still needs to confirm the deletion with the alert
        const handleDelete = async (contact: Contact) => {
            console.log('delete contact', contact);
            // confirm delete with alert
            if(confirm(`Are you sure you want to delete ${contact.name}?`)) {
                fetch('http://localhost:5000/deletecontact', {
                    method: 'POST',
                    headers: {
                    'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(contact)
                })
                .then(response => response.json())
                .then(data => {
                    console.log('Response from backend after post', data);
                    store.setContacts(data);
                });
            };
        };
        /* function to edit contact. Will navigate to edit page and set the mode to edit and 
        the contact state to the contact to be edited */
        const handleEdit = async (contact: Contact) => {
            store.editContact(contact);
            store.setFormMode('edit');
            await router.push('/add');
        }
        // fetch contacts from backend, which comes from MongoDB
        fetch('http://127.0.0.1:5000/getcontacts')
            .then(res => res.json())
            .then(data => {
                store.setContacts(data);
                console.log(data);
            });
        
        return {
            store,
            handleDelete,
            handleEdit
        };
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
        HouseFilled,
        DeleteFilled,
        NButton
        
    }
})
</script>

<template>
    <n-list  clickable class="contactList">
        <n-list-item key="listID++" clickable v-for="contact in store.contacts" class="contactItem">            
            <n-thing content-intended>
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
                <template #header-extra>
                    <!-- Action buttons -->
                    <n-button size="small" class="actionButtonMargin" type="info" @click="handleEdit(contact)" dashed>Edit</n-button>
                    <n-button size="small" class="actionButtonMargin" type="error" @click="handleDelete(contact)">Delete</n-button>
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

<style scoped>
.contactItem {
    padding: 1rem;
    margin: 1rem;
    border : 1px solid #535bf2;
}
.actionButtonMargin {
    margin-right: 0.5rem;
}

</style>