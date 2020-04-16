<template>
  <div class="Login">
    <div v-if="isLoading"></div>

    <form v-else class="LoginForm" @submit.prevent="validation(credentials)">
      <div v-if="getErrors.length" class="error-list alert alert-danger">
        <h4>아래의 오류를 해결해주세요</h4>
        <ul>
          <li v-for="(error, idx) in getErrors" :key="idx">{{ error }}</li>
        </ul>
      </div>

      <div class="LoginForm">
        <h1>Login</h1>
        <ul id="userId">
          <label for="userId">ID</label>
          <input
            v-model="credentials.username"
            type="text"
            id="userId"
            placeholder="아이디"
          />
        </ul>
        <ul id="userPassword">
          <label for="userPassword">Password</label>
          <input
            v-model="credentials.password"
            type="password"
            id="userPassword"
            placeholder="비밀번호"
          />
        </ul>
        <button>로그인</button>
      </div>
      <a href="/signup">Signup</a>
    </form>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex";

export default {
  name: "Login",
  data() {
    return {
      credentials: {
        username: "",
        password: ""
      }
    };
  },
  methods: {
    ...mapActions(["validation"])
  },
  computed: {
    ...mapGetters(["getErrors", "isLoading"])
  }
};
</script>

<style src="./Login.css" scoped></style>
