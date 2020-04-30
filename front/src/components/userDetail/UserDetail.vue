<template>
  <div class="userDetail">
    <v-container class="userCon">
      <v-card
        v-if="getUserInfoModal"
        @close="setUserInfoModal"
        class="userInfoModal"
      >
        <div class="change-pwd" @click="changePwd">
          <v-icon>fas fa-key</v-icon>비밀번호 변경
        </div>
        <div class="change-profil" @click="changeModal">
          <v-icon>fas fa-user-circle</v-icon>프로필사진 변경
        </div>
        <div class="logout" @click="clickLogout">
          <v-icon>fas fa-sign-out-alt</v-icon>로그아웃
        </div>
      </v-card>
      <UserHead />
      <UserInfo />
      <v-card
        v-if="getUserImgModal"
        @close="setUserImgModal"
        class="userImgModal"
      >
        <v-card-title>프로필 사진</v-card-title>
        <input type="file" @change="onFileChange" />
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn class="save" @click="updateUserInfo(PostInfo)">저장</v-btn>
          <v-btn class="close" @click="setUserImgModal">닫기</v-btn>
        </v-card-actions>
      </v-card>
      <CommitCalendar />
      <div class="emotion">
        <h3>Emotion</h3>
        <div class="emotionDetail">감정 분석 결과</div>
      </div>
      <div class="tag">
        <h3>Tag</h3>
        <div class="tagDetail">tag 분석 결과</div>
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
import router from "@/router";

export default {
  name: "UserDetail",
  components: {
    Nav,
    UserHead,
    UserInfo,
    CommitCalendar
  },
  data() {
    return {
      PostInfo: {
        file: null,
        fileName: null
      }
    };
  },
  computed: {
    ...mapGetters([
      "getUserName",
      "getUserId",
      "isLoggedIn",
      "getUserImgModal",
      "getUserInfoModal"
    ])
  },
  methods: {
    ...mapActions(["logout", "updateUserInfo", "logout"]),
    ...mapMutations([
      "setUserImgModal",
      "setUserInfoModal",
      "setUserName",
      "setChanId",
      "setChanName",
      "setPostId"
    ]),
    onFileChange(e) {
      const files = e.target.files;
      if (files) {
        this.PostInfo.file = files[0];
        this.PostInfo.fileName = String(this.getUserId) + ".jpg";
      }
    },
    changePwd() {
      router.push("/changePwd");
    },
    async changeModal() {
      await this.setUserInfoModal();
      this.setUserImgModal();
    },
    clickLogout() {
      this.setChanId(null);
      this.setChanName(null);
      this.setPostId(null);
      sessionStorage.removeItem("chan");
      sessionStorage.removeItem("chanName");
      sessionStorage.removeItem("post");
      this.logout();
    }
  },
  async created() {
    const userName = sessionStorage.getItem("userName");
    if (userName) {
      this.setUserName(userName);
    } else {
      router.push("/");
    }
  },
  destroyed() {
    if (this.getUserInfoModal) {
      this.setUserInfoModal();
    }
    if (this.getUserImgModal) {
      this.setUserImgModal();
    }
  }
};
</script>

<style src="./UserDetail.css" scoped></style>
