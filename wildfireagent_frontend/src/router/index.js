import { createRouter, createWebHistory } from 'vue-router';
import DetailPage from "@/DetailPage.vue";
import DashboardPage from "@/DashboardPage.vue";

const routes = [
  {
    path: '/',
    name: "Dashboard",
    component: DashboardPage
  },
  {
    path: '/detail/:id',
    name: "Detail",
    component: DetailPage,
    props: true
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;