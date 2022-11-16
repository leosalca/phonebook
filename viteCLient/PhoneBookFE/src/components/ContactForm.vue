<script lang="ts">
import { defineComponent, ref } from 'vue'
import { NButton, NForm, NFormItem, NInput } from 'naive-ui'
import { FormInst, FormItemInst, FormItemRule, FormValidationError, FormRules } from 'naive-ui'
import CFBaseInputVue from './CFBaseInput.vue'

export default defineComponent({
    name: 'ContactForm',
    setup() {
        const name = ref('')
        const email = ref('')
        const phone = ref('')
        const company = ref('')
        const address = ref('')
        const city = ref('')
        const state = ref('')
        const zip = ref('')
        const country = ref('')
        const notes = ref('')

        const formRef = ref<FormInst | null>(null)
        return {
            formRef,
            formValue: ref({
                name: '',
                email: '',
                phone: '',
                company: '',
                address: '',
                city: '',
                state: '',
                zip: '',
                country: '',
                notes: ''
            }),
            rules: {
                name: [
                    {
                        required: true,
                        message: 'Name is required'
                    }
                ],
                email: [
                    {
                        required: true,
                        message: 'Email is required'
                    }
                ],
                phone: [
                    {
                        required: true,
                        message: 'Phone is required'
                    }
                ],
                company: [
                    {
                        required: true,
                        message: 'Company is required'
                    }
                ],
                address: [
                    {
                        required: true,
                        message: 'Address is required'
                    }
                ],
                city: [
                    {
                        required: true,
                        message: 'City is required'
                    }
                ],
                state: [
                    {
                        required: true,
                        message: 'State is required'
                    }
                ],
                zip: [
                    {
                        required: true,
                        message: 'Zip is required'
                    }
                ],
                country: [
                    {
                        required: true,
                        message: 'Country is required'
                    }
                ],
                notes: [
                    {
                        required: true,
                        message: 'Notes is required'
                    }
                ]
            },
            
            handleAddContact() {
                
                console.log(formRef.value)
            },
            events: {
                'onUpdate:modelValue': (value: string) => {
                    console.log(value)
                }
            },
            
        }
    },
    components: {
        CFBaseInputVue,
    }
    
})
</script>

<template>
    <!-- make me a vue form component -->
    <div class="contactForm">
        <CFBaseInputVue
            label="Name"
            v-model="formValue.name"
            type="text"
        />
        <pre>
            {{ formValue }}
        </pre>
    </div>
</template>

<style scoped>
.formLabel {
    color: white;
}

.contactForm {
    display: flex;
    flex-direction: column;
    justify-content: center;
    width: 80%;
    margin: 0 auto;

}
</style>