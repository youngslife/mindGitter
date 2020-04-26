<template>
  <div class="userDetail">
    <v-container class="userCon">
      <UserHead />
      <UserInfo />
      <v-card v-if="getUserImgModal" @close="setUserImgModal(false)">
        <v-card-title>프로필 사진</v-card-title>
        <input type="file" />
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn class="save" @click="setUserImgModal(false)">저장</v-btn>
          <v-btn class="close" @click="setUserImgModal(false)">닫기</v-btn>
        </v-card-actions>
      </v-card>
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
import { mapGetters, mapMutations, mapActions } from "vuex";

export default {
  name: "UserDetail",
  components: {
    Nav,
    UserHead,
    UserInfo,
    CommitCalendar
  },
  computed: {
    ...mapGetters(["getUserName", "isLoggedIn", "getUserImgModal"])
  },
  methods: {
    ...mapActions(["logout"]),
    ...mapMutations(["setUserImgModal"])
  }
};
</script>

<style src="./UserDetail.css" scoped></style>
