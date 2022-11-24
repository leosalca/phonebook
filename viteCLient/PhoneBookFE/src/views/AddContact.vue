<script lang='ts'>
    import ContactForm from '../components/ContactForm.vue';
    import { defineComponent } from 'vue';
    export default defineComponent({
        name: 'AddContact',
        setup() {
            return {
                ContactForm
            };
        },
        components: {
            ContactForm
        }
    });
</script>

<template>
    <div class="addContactForm">
        <ContactForm />
    </div>
</template>

<style scoped>
    .addContactForm {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100%;
        background-color: white;
    }
</style>
