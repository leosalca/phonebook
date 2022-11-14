import { createRouter } from "vue-router";
import { createWebHistory } from "vue-router";
import Contacts from "../views/Contacts.vue";
import About from "../views/About.vue";

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: "/",
            name: "Contacts",
            component: Contacts,

        }
    ],
});

export default router;