import { createApp } from 'vue';
import { createPinia } from 'pinia';
import './style.css';
import App from './App.vue';
import router from './router';

// create new app instance
const app = createApp(App);
// bind router to app. Imported from router/index.ts
app.use(router);
// create and bind new pinia instance
app.use(createPinia());
// mount app to #app in index.html
app.mount('#app');