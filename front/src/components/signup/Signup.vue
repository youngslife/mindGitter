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
        <ul id="userId">
          <label for="userId">ID</label>
          <input
            v-model="userInput.userId"
            type="text"
            id="userId"
            placeholder="아이디"
          />
        </ul>
        <ul id="userEmail">
          <label for="userEmail">e-mail</label>
          <input
            v-model="userInput.userEmail"
            type="text"
            id="userEmail"
            placeholder="e-mail"
          />
        </ul>
        <ul id="userPassword">
          <label for="userPassword">Password</label>
          <input
            v-model="userInput.userPassword"
            type="password"
            id="userPassword"
            placeholder="비밀번호"
          />
        </ul>
        <ul id="userPasswordConfirmation">
          <label for="userPasswordConfirmation">Password</label>
          <input
            v-model="userInput.userPasswordConfirmation"
            type="password"
            id="userPasswordConfirmation"
            placeholder="비밀번호확인"
          />
        </ul>
        <button>회원가입</button>
      </div>
      <a href="/login">Login</a>
    </form>
  </div>
</template>

<script>
import { mapGetters, mapMutations, mapActions } from "vuex";

export default {
  name: "Signup",
  data() {
    return {
      userInput: {
        userId: "",
        userEmail: "",
        userPassword: "",
        userPasswordConfirmation: ""
      }
    };
  },
  methods: {
    ...mapActions(["signup"]),
    ...mapMutations(["clearErrors"])
  },
  computed: {
    ...mapGetters(["getErrors"])
  }
};
</script>

<style src="./Signup.css" scoped></style>
