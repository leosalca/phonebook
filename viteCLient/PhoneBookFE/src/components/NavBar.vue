<script lang="ts">
import { defineComponent } from 'vue';
import { PersonAddSharp, CancelFilled } from '@vicons/material';
import { NButton, NIcon } from 'naive-ui';
import {  useRouter } from 'vue-router';
import { useContactStore } from '../stores/useContactStore';


export default defineComponent({
    name: 'NavBar',
    setup() {
        // define router to navigate to different routes from NavBar
        const router = useRouter();
        // define store to access states and actions from store
        const store = useContactStore();

        // function will navigate to add contact page, clear the contact state and set the mode to add
        const handleAddContact = async () => {
            store.clearEditContact();
            store.setFormMode('add');
            console.log(store.editCurrentContact);
            await router.push('/add');
            console.log('handleAdd clicked')
        };

        const handleCancel = async () => {
            store.clearEditContact();
            store.setFormMode('add');
            await router.push('/');
        };
        return { handleAddContact, handleCancel ,store };
    },
    components: {
        NButton,
        NIcon,
        PersonAddSharp,
        CancelFilled
    }
})

</script>
<template>
    <nav class="navigation">
        <router-link to="/">Contacts</router-link>
        <div>
            <n-button v-if="store.formMode === 'edit' " class="cancelEditButton" circle @click="handleCancel()">
                    <n-icon><CancelFilled /></n-icon>
            </n-button>
            <n-button v-if="store.formMode === 'add'" class="addButton" circle ghost @click="handleAddContact()" >
                <template #icon>
                    <n-icon><PersonAddSharp/></n-icon>
                </template>
            </n-button>
        </div>
    </nav>
</template>

<style scoped>
.navigation {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  padding: 0 1rem;
  height: 3rem;
  background-color: #535bf2;
  margin-bottom: 1rem;
}

.addButton {
  color: white;
}
.addButton:hover {
  color: #36ad6a
}
.cancelEditButton {
    color: red;
}
.cancelEditButton:hover {
    color: white;
    background-color: red;
}
</style>
