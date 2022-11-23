<script lang="ts">
import { defineComponent, ref, computed } from 'vue'
import CFBaseInputVue from './CFBaseInput.vue'
import { useVuelidate } from '@vuelidate/core'
import { required, minLength, email } from '@vuelidate/validators'
import { Contact, Address } from '../types/contact'
import {  useRouter } from 'vue-router'
import { useContactStore } from '../stores/useContactStore'


export default defineComponent({
    name: 'ContactForm',
    emits: ['submit'],
    setup() {
        
        // store instance
        const store = useContactStore()

        const editContact = store.editCurrentContact

        const formMode = store.formMode
        
        const router = useRouter()
        const formValue = ref({
            name: editContact.name||'',
            email: editContact.email||'',
            phone: editContact.phone||'',
            company: editContact.company||'',
            address: {
                street: editContact.address?.street||'',
                city: editContact.address?.city||'',
                zipcode: editContact.address?.zipcode||'',
                state: editContact.address?.state||'',
                country: editContact.address?.country||'',
            },
            id: editContact.id ||''
        })
        
        console.log('edit contact', editContact)
        //assign edit contact to form value

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
                zipcode: {
                    minLength: minLength(5),
                    required
                },
                country: {
                    required
                }
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
                    if (formMode === 'add'){
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
                    } else if (formMode === 'edit') {
                        fetch("http://127.0.0.1:5000/updatecontact", {
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
                    }
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
            uspsVerification,
            formMode
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
            v-model="formValue.address.zipcode"
            type="text"
            @blur="v$.address.zipcode.$touch()"
            />
            <button v-if="v$.address.zipcode.$error === false && v$.address.zipcode.$dirty" class="verifyButton" @click.prevent="verifyWithUsps(formValue.address.zipcode)">Verify</button>
        </div>
        <div v-if="v$.address.zipcode.$error" class="errorMsg" v-for="error of v$.address.zipcode.$errors" :key="error.$uid">
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

        <button v-if="formMode === 'add'" type="submit" class="submitButton">Save</button>
        <button v-if="formMode === 'edit'" type="submit" class="submitButton">Update</button>
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
.errorMsg {
  color: red;
  font-size: 0.75rem;
  font-weight: 600;
  margin-left: 4rem;
}
.verMsg {
  color: white;
  font-size: 0.75rem;
  font-weight: 600;
  margin: auto;
}
.submitButton {
    background-color: #4CAF50; /* Green */
    border: none;
    border-radius: 5px;
    color: white;
    text-align: center;
    text-decoration: none;
    font-size: 16px;
    margin: 1rem;
    cursor: pointer;
    height: 35px;
    width: 40%;
    align-self: center;
}
</style>