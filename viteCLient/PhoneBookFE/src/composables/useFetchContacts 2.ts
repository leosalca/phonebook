import { ref } from 'vue';
import type { Contact } from '../types/contact';

export function useFetchContacts(url: string | null) {
    let contacts = ref<Contact[]>([]);
    const error = ref(null);

    if (url !== null) {
    fetch(url)
        .then(res => {
            if (!res.ok) {
                throw Error('Could not fetch the data for that resource');
            }
            return res.json();
        })
        .then(data => {
            contacts.value = data;
            error.value = null;
        })
    }
    return { contacts, error };
};

