<template>
  <div class="changePwd">
    <v-icon @click="backPage">fas fa-arrow-circle-left</v-icon>
    <h1>비번 변경 페이지</h1>
    <form @submit.prevent="changePwd(PasswordInfo)">
      <div>
        <label for="oldpassword">기존 비밀번호</label>
        <br />
        <input v-model="PasswordInfo.oldPassword" type="password" />
      </div>
      <div>
        <label for="oldpassword">새 비밀번호</label>
        <br />
        <input v-model="PasswordInfo.newPassword1" type="password" />
      </div>
      <div>
        <label for="oldpassword">비밀번호 확인</label>
        <br />
        <input v-model="PasswordInfo.newPassword2" type="password" />
      </div>
      <button>변경하기</button>
    </form>
  </div>
</template>

<script>
import router from "@/router";
import { mapActions } from "vuex";

export default {
  name: "changePwd",
  data() {
    return {
      PasswordInfo: {
        oldPassword: null,
        newPassword1: null,
        newPassword2: null
      }
    };
  },
  methods: {
    ...mapActions(["changePwd"]),
    backPage() {
      router.go(-1);
    }
  }
};
</script>

<style src="./ChangePwd.css" scoped></style>