import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Contact } from '../types/contact'


export const useContactStore = defineStore('contact',() => {
    const contacts = ref<Contact[]>([]);

    const setContacts = (newContacts: Contact[]) => {
        contacts.value = newContacts;
    }

    // const fetchContacts = async () => {
    //     fetch('http://127.0.0.1:5000/getcontacts')
    //         .then(response => response.json())
    //         .then(json => setContacts(json))
        
        
    // }

    return {
        contacts,
        setContacts
    }
})
