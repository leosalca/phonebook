<script lang="ts">
import { defineComponent, ref, computed } from 'vue'
import CFBaseInputVue from './CFBaseInput.vue'
import { useVuelidate } from '@vuelidate/core'
import { required, minLength, email } from '@vuelidate/validators'

export default defineComponent({
    name: 'ContactForm',
    emits: ['submit'],
    setup() {
        
        const formValue = ref({
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
        })

        const rules = computed(() => ({
            name: {
                required,
                minLength: minLength(2)
            },
            email: {
                email
            },
            phone: {
                required,
                minLength: minLength(10)
            },
            company: {
                required
            },
            address: {
                required
            },
            city: {
                required
            },
            state: {
                required
            },
            zip: {
                required
            },
            country: {
                required
            },
            notes: {
                required
            }
        
        }))

        const v$ = useVuelidate(rules, formValue)


        const onSubmit = async () => {
            console.log(formValue.value)
            const isFormCorrect = await v$.value.$validate()
            console.log(v$.value)
            if (isFormCorrect) {
                console.log('Form is valid')
            } else {
                console.log('Form is invalid')
                alert('Form is invalid')
                return
            }
        }

        return {
            onSubmit,
            formValue,
            v$,
        }
    },
    components: {
        CFBaseInputVue,
    }
   
    
})
</script>

<template>
    <!-- make me a vue form component -->
    <form class="contactForm" >
        <CFBaseInputVue
            label="Name"
            v-model="formValue.name"
            type="text"
            @blur="v$.name.$touch()"
        />
        <div v-if="v$.name.$error" class="errorMsg">Name field has an error</div>
        <CFBaseInputVue
            label="Email"
            v-model="formValue.email"
            type="email"
            @blur="v$.email.$touch()"
        />
        <div v-if="v$.email.$error" class="errorMsg">Email field has an error</div>
        <CFBaseInputVue
            label="Phone"
            v-model="formValue.phone"
            type="tel"
            @blur="v$.phone.$touch()"
        />
        <div v-if="v$.phone.$error" class="errorMsg">Phone field has an error</div>
        <CFBaseInputVue
            label="Company"
            v-model="formValue.company"
            type="text"
            @blur="v$.company.$touch()"
        />
        <div v-if="v$.company.$error" class="errorMsg">Company field has an error</div>
        <CFBaseInputVue
            label="Address"
            v-model="formValue.address"
            type="text"
            @blur="v$.address.$touch()"
        />
        <div v-if="v$.address.$error" class="errorMsg">Address field has an error</div>
        <CFBaseInputVue
            label="City"
            v-model="formValue.city"
            type="text"
            @blur="v$.city.$touch()"
        />
        <div v-if="v$.city.$error" class="errorMsg">City field has an error</div>
        <CFBaseInputVue
            label="State"
            v-model="formValue.state"
            type="text"
            @blur="v$.state.$touch()"
        />
        <div v-if="v$.state.$error" class="errorMsg">State field has an error</div>
        <CFBaseInputVue
            label="Zip"
            v-model="formValue.zip"
            type="text"
            @blur="v$.zip.$touch()"
        />
        <div v-if="v$.zip.$error" class="errorMsg">Zip field has an error</div>
        <CFBaseInputVue
            label="Country"
            v-model="formValue.country"
            type="text"
            @blur="v$.country.$touch()"
        />
        <div v-if="v$.country.$error" class="errorMsg">Country field has an error</div>
        <CFBaseInputVue
            label="Notes"
            v-model="formValue.notes"
            type="text"
            @blur="v$.notes.$touch()"
        />
        <div v-if="v$.notes.$error" class="errorMsg">Notes field has an error</div>
        <button @click.prevent="onSubmit(formValue)">Submit</button>
    </form>
    
    <pre>
        {{ formValue }}
    </pre>
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