import { ref } from 'vue'
import type { Contact } from '../types/contact'

export function useFetch(url: string) {
    const contacts = ref<Contact[]>([])
    const error = ref(null)

    fetch(url)
        .then(res => {
            if (!res.ok) {
                throw Error('Could not fetch the data for that resource')
            }
            return res.json()
        })
        .then(data => {
            contacts.value = data
            error.value = null
        })
    return { contacts, error }
}