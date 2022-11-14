import { createRouter } from "vue-router";
import { createWebHistory } from "vue-router";
import Home from "../views/Home.vue";
import About from "../views/About.vue";

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/home',
            name: 'Home',
            component: Home ,
        },
    ],
});

export default router;