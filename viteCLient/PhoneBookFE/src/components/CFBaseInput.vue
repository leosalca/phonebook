<!-- Reusable component used in ContactForm -->
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
import { defineComponent } from 'vue';

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
});
</script>

<style scoped>
.baseInput {
  width: 80%;
  display: flex;
  align-self: center;
  flex-direction: column;
}
.baseInput input {
  min-width: 50%;
  padding: 0.5rem;
  margin: 0.5rem 0.5rem;
  border: 1px solid #535bf2;
  border-radius: 0.25rem;
  background-color: #f9f9f9;
  color: #213547;
}
.baseInput label {
  font-size: 1rem;
  font-weight: 600;
  color: #f9f9f9;
}

</style>

