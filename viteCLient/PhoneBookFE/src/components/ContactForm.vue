<script lang="ts">
import { defineComponent, ref, computed } from 'vue'
import CFBaseInputVue from './CFBaseInput.vue'
import { useVuelidate } from '@vuelidate/core'
import { useFetchContacts } from '../composables/useFetchContacts'
import { required, minLength, email, requiredIf, helpers } from '@vuelidate/validators'
import { Contact } from '../types/contact'
import {  useRouter } from 'vue-router'
import { onMounted } from 'vue'
import { useContactStore } from '../stores/useContactStore'


export default defineComponent({
    name: 'ContactForm',
    emits: ['submit'],
    setup() {
        
        // store instance
        const store = useContactStore()
        
        const router = useRouter()
        const formValue = ref({
            name: '',
            email: '',
            phone: '',
            company: '',
            address: {
                street: '',
                city: '',
                state: '',
                zip: '',
                country: ''
            },
            notes: ''
        })
        
        const uspsVerification = ref(false)

        const rules = computed(() => ({
            name: {
                required,
                minLength: minLength(2), //add a custom message
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
                street: {
                    required
                },
                city: {
                    required
                },
                state: {
                    required
                },
                zip: {
                    minLength: minLength(5),
                    required
                },
                country: {
                    required
                }
            },
            notes: {
                required
            }
        
        }))

        const v$ = useVuelidate(rules, formValue)

        // Form values are validated on submit, and if valid, the form is submitted to backend
        const onSubmit = async (FormData: Contact) => {
            console.log(FormData)
            const jsonData = JSON.stringify(FormData)
            console.log(jsonData)
            const isFormCorrect = await v$.value.$validate()
            const isUSPSValid = uspsVerification.value
            console.log(v$.value)
            if (isFormCorrect) {
                console.log('Form is valid')
                
                // Submit form to backend
                if (isUSPSValid) {
                    fetch("http://127.0.0.1:5000/addcontact", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"

                    },
                    body: jsonData
                    })
                    .then(response => response.json())
                    .then(data => {                    
                        console.log('Response from backend after post', data)
                        store.setContacts(data)
                    })
                } else {
                    console.log('USPS verification failed')
                    alert('USPS verification failed, pleasy try again')
                    return
                }
                

            } else {
                console.log('Form is invalid')
                alert('Form is invalid')
                return
            }
            await router.push('/')
        }

        const verifyWithUsps = async (zip: String) => {
            console.log('Verify with USPS')
            console.log(zip)
            fetch("http://127.0.0.1:5000/verifyzip", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"

                },
                body: JSON.stringify({zip: zip})
            })
            .then(response => response.json())
            .then(data => {
                console.log('Response from backend after post', data, uspsVerification)
                if (data.city){
                    uspsVerification.value = true
                }
                formValue.value.address.city = data.city
                formValue.value.address.state = data.state
            })
        }

        return {
            onSubmit,
            verifyWithUsps,
            formValue,
            v$,
            uspsVerification
        }
    },
    components: {
        CFBaseInputVue,
    },
   
})
</script>

<template>
    <!-- make me a vue form component -->
    <form class="contactForm" @submit.prevent="onSubmit(formValue)">
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
        <div v-if="v$.email.$error" class="errorMsg">Please enter a valid email address</div>

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
            label="Street"
            v-model="formValue.address.street"
            type="text"
            @blur="v$.address.street.$touch()"
        />
        <div v-if="v$.address.street.$error" class="errorMsg">Street field has an error</div>

        <CFBaseInputVue
            label="City"
            v-model="formValue.address.city"
            type="text"
            @blur="v$.address.city.$touch()"
        />
        <div v-if="v$.address.city.$error" class="errorMsg">City field has an error</div>

        <CFBaseInputVue
            label="State"
            v-model="formValue.address.state"
            type="text"
            @blur="v$.address.state.$touch()"
        />
        <div v-if="v$.address.state.$error" class="errorMsg">State field has an error</div>

        <div class="zipContainer">
            <CFBaseInputVue
            label="Zip"
            v-model="formValue.address.zip"
            type="text"
            @blur="v$.address.zip.$touch()"
            />
            <button v-if="v$.address.zip.$error === false && v$.address.zip.$dirty" class="verifyButton" @click.prevent="verifyWithUsps(formValue.address.zip)">Verify</button>
        </div>
        <div v-if="v$.address.zip.$error" class="errorMsg" v-for="error of v$.address.zip.$errors" :key="error.$uid">
            {{error.$message}}
            <div v-if="!uspsVerification" class="verMsg">Once typed, please verify zipcode with USPS</div>
        </div>
        <div v-if="uspsVerification" class="verMsg">Zipcode verified with USPS</div>
        <CFBaseInputVue
            label="Country"
            v-model="formValue.address.country"
            type="text"
            @blur="v$.address.country.$touch()"
        />
        <div v-if="v$.address.country.$error" class="errorMsg">Country field has an error</div>

        <CFBaseInputVue
            label="Notes"
            v-model="formValue.notes"
            type="text"
            @blur="v$.notes.$touch()"
        />
        <div v-if="v$.notes.$error" class="errorMsg">Notes field has an error</div>

        <button type="submit">Submit</button>
    </form>
</template>

<style scoped>
.verifyButton {
    background-color: #4CAF50; /* Green */
    border: none;
    color: white;
    text-align: center;
    text-decoration: none;
    font-size: 16px;
    margin: 0.5rem;
    cursor: pointer;
    height: 35px;
    align-self: flex-end;
}

.contactForm {
    display: flex;
    flex-direction: column;
    justify-content: center;
    width: 80%;
    margin: 0 auto;
}

.zipContainer {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    width: 80%;
    align-self: center;
    margin: 0.5rem 0.5rem;
}
 
</style>