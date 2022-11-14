import { ref } from 'vue'
import type { Contact } from '../types/contact'

export function useFetch(url: string) {
    const data = ref<Contact[]>([])
    const error = ref(null)
    
    fetch(url)
        .then(res => {
            if (!res.ok) {
                throw Error('Could not fetch the data for that resource')
            }
            return res.json()
        })
        .then((res) => {
            data.value = res
            error.value = null
        })
        .catch(err => {
            console.log(err.message)
            error.value = err.message
        })

    return { data, error }
}