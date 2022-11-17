<script lang='ts'>
    import ContactForm from '../components/ContactForm.vue';
    import { defineComponent, ref } from 'vue';
    export default defineComponent({
        name: 'AddContact',
        setup() {
            return {
                ContactForm
            }
        },
        components: {
            ContactForm
        }
    })
</script>

<template>
    <div class="addContact">
        <ContactForm />
    </div>
</template>

<style scoped>
    .addContact {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100%;
        background-color: white;
    }
</style>
