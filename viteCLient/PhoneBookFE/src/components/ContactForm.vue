<script lang="ts">
import { defineComponent, ref, computed, reactive } from 'vue';
import CFBaseInputVue from './CFBaseInput.vue';
import { useVuelidate } from '@vuelidate/core';
import { required, minLength, email } from '@vuelidate/validators';
import { Contact, Address } from '../types/contact';
import {  useRouter } from 'vue-router';
import { useContactStore } from '../stores/useContactStore';


export default defineComponent({
    name: 'ContactForm',
    emits: ['submit'],
    setup() {
        
        // store instance to access states and actions from store
        const store = useContactStore();
        // define contact needed to be edited. Value comes from store.
        const editContact =  store.editCurrentContact;
        // define formMode. Value comes from store and it can be 'add' or 'edit'. Button shown will change according to this value.
        const formMode = store.formMode;
        /* define router to navigate to different routes from ContactForm. 
        When contact is added or edited, it will navigate to home page.*/
        const router = useRouter();
        /* define contact object to be used in form as a vue reactive value. As the form is filled, values are assigned
        If editContact has value, the form is prepopulated with them.*/
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
        });
        
        console.log('edit contact', editContact);

        /* USPS Zipcode API validation. Value changes to true when zip code input is validated using the verify button.
        If the value is true, the form can be submitted. */
        const uspsVerification = ref(false);

        // define vuelidate rules for form validation
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
                street: {required}, city: {required}, state: {required}, zipcode: { minLength: minLength(5), required }, country: {required}
            }
        }));
        // define vuelidate instance, passing the formValue and rules. If form has errors, they can be accessed from $v
        const v$ = useVuelidate(rules, formValue);

        /* function will check if the form has errors and if USPS verification is true. 
        If both are true, it will then check if its a new contact or editing a current one.
        It will then submit to the appropriate api route. Response from API refreshes contact list.
        Router then navigates to home*/
        const onSubmit = async (FormData: Contact) => {
            console.log(FormData);
            // getting data ready to be sent to API
            const jsonData = JSON.stringify(FormData);
            console.log(jsonData);
            // run through vuelidate to check for errors, returns true if there are no errors
            const isFormCorrect = await v$.value.$validate();
            // extracting value from uspsVerification to check if it is true later
            const isUSPSValid = uspsVerification.value;
            console.log(v$.value);
            // first check if form is valid, return if not and alert user
            if (isFormCorrect) {
                console.log('Form is valid');
                // second check if usps verification is true, return if not and alert user. Use verify button to validate zipcode
                if (isUSPSValid) {
                    /* at this point form is valid and usps verification is true, 
                    now check if its a new contact or editing a current one.
                    Send to the appropriate route.*/
                    if (formMode === 'add'){
                        fetch("http://127.0.0.1:8000/addcontact", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: jsonData
                        })
                        .then(response => response.json())
                        .then(data => {                    
                            console.log('Response from backend after post', data);
                            // refresh contact list
                            store.setContacts(data);
                        });
                    } else if (formMode === 'edit') {
                        fetch("http://127.0.0.1:8000/updatecontact", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: jsonData
                        })
                        .then(response => response.json())
                        .then(data => {                    
                            console.log('Response from backend after post', data);
                            store.setContacts(data);
                        });
                    };
                } else {
                    console.log('USPS verification failed');
                    alert('USPS verification failed, pleasy try again');
                    return
                };
            } else {
                console.log('Form is invalid');
                alert('Form is invalid');
                return
            };
            await router.push('/'); // navigate to home page after form is submitted
        };
        // function to validate zipcode using USPS API
        const verifyWithUsps = async (zip: String) => {
            console.log('Verify with USPS');
            console.log(zip);
            fetch("http://127.0.0.1:8000/verifyzip", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({zip: zip})
            })
            .then(response => response.json())
            .then(data => {
                console.log('Response from backend after post', data, uspsVerification);
                if (data.city){
                    // if city is returned, zipcode is valid
                    uspsVerification.value = true;
                };
                // assign city and state from USPS to formValue
                formValue.value.address.city = data.city;
                formValue.value.address.state = data.state;
            });
        };

        return {
            onSubmit,
            verifyWithUsps,
            formValue,
            v$,
            uspsVerification,
            formMode
        };
    },
    components: {
        CFBaseInputVue,
    },
   
});
</script>
<!-- Form inputs run through validation when the user clicks out of the field
or when the form is submitted. If there are errors, they are shown below the input field. 
The value here is binded to the formValue reactive value-->
<template>
    <form ref="contactForm" class="contactForm" @submit.prevent="onSubmit(formValue)">
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
        <!-- formMode store value dictates what button is shown -->
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