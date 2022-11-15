import { ref } from 'vue'
import type { Contact } from '../types/contact'

export function useFetch(url: string) {
    const data = ref<Contact[]>([])
    const error = ref(null)
    
    fetch(url)
        .then(res => res.json())
        .then(res => data.value = res.contacts)
        .catch(err => error.value = err)


    return { data, error }
}