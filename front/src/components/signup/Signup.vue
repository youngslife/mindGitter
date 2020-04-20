<template>
  <div class="Signup">
    <form class="SignupForm" @submit.prevent="signup(userInput)">
      <div class="SignupForm">
        <h1>Signup</h1>
        <div v-if="getErrors.length" class="error-list alert alert-danger">
          <p>아래의 오류를 해결해주세요</p>
          <ul>
            <li v-for="(error, idx) in getErrors" :key="idx">
              {{ error }}
            </li>
          </ul>
        </div>
        <ul id="username">
          <label for="username">ID</label
          ><br />
          <input
            v-model="userInput.username"
            type="text"
            id="username"
            placeholder="아이디"
          />
        </ul>
        <ul id="email">
          <label for="email">e-mail</label
          ><br />
          <input
            v-model="userInput.email"
            type="text"
            id="email"
            placeholder="e-mail"
          />
        </ul>
        <ul id="password1">
          <label for="password1">Password</label
          ><br />
          <input
            v-model="userInput.password1"
            type="password"
            id="password1"
            placeholder="비밀번호"
          />
        </ul>
        <ul id="password2">
          <label for="password2">Password</label
          ><br />
          <input
            v-model="userInput.password2"
            type="password"
            id="password2"
            placeholder="비밀번호확인"
          />
        </ul>
        <button>회원가입</button>
      </div>
      <button @click="goLogin">Login</button>
    </form>
  </div>
</template>

<script>
import { mapGetters, mapMutations, mapActions } from "vuex";
import router from "@/router";
export default {
  name: "Signup",
  data() {
    return {
      userInput: {
        username: "",
        email: "",
        password1: "",
        password2: "",
      },
    };
  },
  methods: {
    ...mapActions(["signup"]),
    ...mapMutations(["clearErrors"]),
    goLogin() {
      router.push("/login");
    },
  },
  computed: {
    ...mapGetters(["getErrors"]),
  },
};
</script>

<style src="./Signup.css" scoped></style>
