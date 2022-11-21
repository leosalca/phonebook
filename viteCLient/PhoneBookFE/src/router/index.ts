import { createRouter,  } from "vue-router";
import { createWebHistory } from "vue-router";
import Contacts from "../views/Contacts.vue";
import AddContact from "../views/AddContact.vue";
import About from "../views/About.vue";

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: "/",
            name: "Contacts",
            component: Contacts,
            
        },
        {
            path: "/add",
            name: "AddContact",
            component: AddContact,
        },
    ],
});

export default router;