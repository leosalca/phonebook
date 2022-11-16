<template >
    <label>{{ label }}</label>
    <input
        :placeholder="label"
        :value="modelValue"
        v-bind="$attrs"
        @input="$emit('update:modelValue', $event.target.value)"
    >
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
import { NForm, NFormItem, NInput } from 'naive-ui'
import { Contact, Address } from '../types/Contact'


export default defineComponent({
    props: {
        label: {
            type: String,
            default: ''
        },
        modelValue: {
            type: [String, Number],
            default: ''
        }
    },
    components: {
        
    }
})
</script>