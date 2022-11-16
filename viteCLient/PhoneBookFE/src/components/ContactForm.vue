<script lang="ts">
import { defineComponent, ref } from 'vue'
import { NButton, NForm, NFormItem, NInput, NSelect, NDatePicker, NTimePicker, NInputNumber, NCheckbox, NCheckboxGroup, NRadio, NRadioGroup, NRate, NSwitch, NSlider, NUpload, NDivider, NSpace, NCard, NAvatar, NIcon, NList, NListItem, NThing } from 'naive-ui'

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

        const addContact = () => {
            console.log(name.value)
        }

        return {
            name, email, phone, company, address, city, state, zip, country, notes, addContact
        }
    },
    props: {
        name: String,
        email: String,
        phone: String,
        company: String,
        address: String,
        city: String,
        state: String,
        zip: String,
        country: String,
        notes: String
    },
    components: {
        NButton,
        NForm,
        NFormItem,
        NInput,
        NSelect,
        NDatePicker,
        NTimePicker,
        NInputNumber,
        NCheckbox,
        NCheckboxGroup,
        NRadio,
        NRadioGroup,
        NRate,
        NSwitch,
        NSlider,
        NUpload,
        NDivider,
        NSpace,
        NCard,
        NAvatar,
        NIcon,
        NList,
        NListItem,
        NThing,
    }
})
</script>

<template>
    <!-- make me a vue form component -->
    <div class="contactForm">
        <n-form>
            <n-form-item label="Name" class="formLabel">
                <n-input v-model:value="name" />
            </n-form-item>
            <n-form-item label="Email" class="formLabel">
                <n-input v-model:value="email" />
            </n-form-item>
            <n-form-item label="Phone" class="formLabel">
                <n-input v-model:value="phone" />
            </n-form-item>
            <n-form-item label="Company" class="formLabel">
                <n-input v-model:value="company" />
            </n-form-item>
            <n-form-item label="Address" class="formLabel">
                <n-input v-model:value="address" />
            </n-form-item>
            <n-form-item label="City" class="formLabel">
                <n-input v-model:value="city" />
            </n-form-item>
            <n-form-item label="State" class="formLabel">
                <n-input v-model:value="state" />
            </n-form-item>
            <n-form-item label="Zip" class="formLabel">
                <n-input v-model:value="zip" />
            </n-form-item>
            <n-form-item label="Country" class="formLabel">
                <n-input v-model:value="country" />
            </n-form-item>
            <n-form-item label="Notes" class="formLabel">
                <n-input v-model:value="notes" />
            </n-form-item>
            <n-form-item>
                <n-button type="primary" @click="addContact">Add Contact</n-button>
            </n-form-item>
        </n-form>
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