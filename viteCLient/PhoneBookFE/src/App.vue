<script setup lang="ts">

import { PersonAddSharp } from '@vicons/material'
import { NButton, NIcon } from 'naive-ui'
import { ref } from 'vue'
import { useFetch } from './store/store';

const addContact = () => {
    console.log('add contact')
}

</script>

<template>
  <nav class="navigation">
    <router-link to="/">Contacts</router-link>
    <n-button class="addButton" circle ghost @click="addContact()">
      <template #icon>
        <n-icon><PersonAddSharp/></n-icon>
      </template>
    </n-button>
  </nav>
  <router-view/>
</template>

<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
