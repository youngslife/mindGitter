<template>
  <div class="userDetail">
    <v-container class="userCon">
      <UserHead />
      <UserInfo />
      <CommitCalendar />
      <div class="emotion">
        <h3>Emotion</h3>
        <div class="emotionDetail">
          감정 분석 결과
        </div>
      </div>
      <div class="tag">
        <h3>Tag</h3>
        <div class="tagDetail">
          tag 분석 결과
        </div>
      </div>
    </v-container>
    <Nav />
  </div>
</template>

<script>
import Nav from "../nav/Nav.vue";
import UserHead from "./userInfo/UserHead.vue";
import UserInfo from "./userInfo/UserInfo.vue";
import CommitCalendar from "./userInfo/CommitCalendar";
import { mapGetters, mapActions } from "vuex";

export default {
  name: "UserDetail",
  components: {
    Nav,
    UserHead,
    UserInfo,
    CommitCalendar,
  },
  computed: {
    ...mapGetters(["getUserName", "isLoggedIn"])
  },
  methods: {
    ...mapActions(["logout"])
  }
};
</script>

<style src="./UserDetail.css" scoped></style>
