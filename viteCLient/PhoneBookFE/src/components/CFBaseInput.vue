<template>
    <div class="baseInput">
        <label>{{ label }}</label>
        <input
            :placeholder="label"
            :value="modelValue"
            :rules="rules"
            v-bind="$attrs"
            @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
        >
    </div>
</template>

<script lang="ts">
import { defineComponent, ref, defineEmits } from 'vue'

export default defineComponent({
    props: {
        label: {
            type: String,
            default: ''
        },
        modelValue: {
            type: [String, Number],
            default: ''
        },
        rules : {
            type: Array,
        }
    },
})
</script>

