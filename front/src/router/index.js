import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../components/home/Home.vue";
import CreateDiary from "../components/createDiary/createDiary.vue";
import DiaryDetail from "../components/diaryDetail/DiaryDetail.vue";
import DiaryList from "../components/diaryList/DiaryList.vue";
import Login from "../components/login/Login.vue";
import NewDiary from "../components/newDiary/NewDiary.vue";
import UserDetail from "../components/userDetail/UserDetail.vue";
import Signup from "../components/signup/Signup.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/signup",
    name: "Signup",
    component: Signup
  },
  {
    path: "/createDiary",
    name: "CreateDiary",
    component: CreateDiary
  },
  {
    path: "/diaryDetail",
    name: "DiaryDetail",
    component: DiaryDetail
  },
  {
    path: "/diaryList",
    name: "DiaryList",
    component: DiaryList
  },
  {
    path: "/newDiary",
    name: "NewDiary",
    component: NewDiary
  },
  {
    path: "/login",
    name: "Login",
    component: Login
  },
  {
    path: "/userDetail",
    name: "userDetail",
    component: UserDetail
  },
  {
    path: "/",
    name: "home",
    component: Home
  }
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes
});

export default router;
