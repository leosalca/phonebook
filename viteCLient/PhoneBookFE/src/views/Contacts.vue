<script lang="ts">
    import ContactList from '../components/ContactList.vue';
    import { defineComponent } from 'vue';
    export default defineComponent({
        name: 'Contact',
        setup() {
            return {
                ContactList
            };
        },
        components: {
            ContactList
        }
    });
</script>

<template>
    <ContactList />
</template>