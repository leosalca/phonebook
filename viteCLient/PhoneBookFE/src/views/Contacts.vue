<script lang="ts">
    import ContactList from '../components/ContactList.vue'
    import { defineComponent, ref } from 'vue'
    export default defineComponent({
        name: 'Contact',
        setup() {
            return {
                ContactList
            }
        },
        components: {
            ContactList
        }
    })
</script>

<template :contacts="contacts">
    <ContactList />
</template>