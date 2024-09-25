import MainPage from "@/pages/MainPage";
import FormPage from "@/pages/FormPage";
import ResultPage from "@/pages/ResultPage";
import {createRouter, createWebHistory} from "vue-router";

const routes = [
    {
        path: '/v1',
        name: "main-page",
        component: MainPage,
    },
    {
        path: '/v1/form',
        name: "form-page-default",
        component: FormPage,
    },
    {
        path: '/v1/form/:printSet',
        name: "form-page",
        component: FormPage,
    },
    {
        path: '/v1/result',
        name: "result-page",
        component: ResultPage,
    },
]


const router = createRouter({
    routes,
    history: createWebHistory('/')
    //history: createWebHistory(process.env.BASE_URL)
})

export default router;