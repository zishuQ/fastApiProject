import Statistic from "@/components/Statistic.vue";
import { createRouter, createWebHistory } from 'vue-router';
import App from "@/App.vue";

const router = createRouter({
    history: createWebHistory(),
    routes: [
        // 定义你的路由规则
        {
            path: "/",
            component: App
        },
        {
            path: "/statistics",
            component: Statistic
        }
    ],
});


export default router
