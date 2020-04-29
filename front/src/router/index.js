import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../components/home/Home.vue";
import CreateDiary from "../components/createDiary/createDiary.vue";
import DiaryDetail from "../components/diaryDetail/DiaryDetail.vue";
import PostList from "../components/postList/PostList.vue";
import Login from "../components/login/Login.vue";
import NewPost from "../components/newPost/NewPost.vue";
import UserDetail from "../components/userDetail/UserDetail.vue";
import Signup from "../components/signup/Signup.vue";
import EditPost from "../components/editPost/editPost.vue";
import EditChan from "../components/editDiary/editDiary";
import ChangePwd from "../components/userDetail/ChangePwd.vue";

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
    path: "/postList",
    name: "PostList",
    component: PostList
  },
  {
    path: "/newPost",
    name: "NewPost",
    component: NewPost
  },
  {
    path: "/login",
    name: "Login",
    component: Login
  },
  {
    path: "/userDetail",
    name: "UserDetail",
    component: UserDetail
  },
  {
    path: "/",
    name: "home",
    component: Home
  },
  {
    path: "/editPost",
    name: "editPost",
    component: EditPost
  },
  {
    path: "/editChan",
    name: "editChan",
    component: EditChan
  },
  {
    path: "/changePwd",
    name: "changePwd",
    component: ChangePwd
  }
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes
});

export default router;
