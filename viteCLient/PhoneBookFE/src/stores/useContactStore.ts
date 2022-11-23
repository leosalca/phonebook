import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Contact } from '../types/contact'


export const useContactStore = defineStore('contact',() => {
    const contacts = ref<Contact[]>([]);
    const editCurrentContact = ref<Contact>({} as Contact)
    const formMode = ref('add');

    const setContacts = (newContacts: Contact[]) => {
        contacts.value = newContacts;
    }
    const editContact = (contact: Contact) => {
        editCurrentContact.value = contact;
    }

    const clearEditContact = () => {
        editCurrentContact.value = {} as Contact;
    }

    const setFormMode = (mode: string) => {
        formMode.value = mode;
    }
    return {
        contacts,
        editCurrentContact,
        formMode,
        editContact,
        setContacts,
        setFormMode,
        clearEditContact
    }
})
