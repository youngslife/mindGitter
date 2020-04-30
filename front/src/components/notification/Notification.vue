<template>
  <div class="nContainer">
    <div class="nBar">
      <div class="nBtn nBackBtn" @click="goHome">
        <v-icon color="rgba(0, 0, 0, 0.5)" small>fas fa-arrow-left</v-icon>
      </div>
      <p class="nDate">알림함</p>
    </div>
    <div v-if="getNotiList && getNotiList.length" class="nContentBox">
      <div v-for="(item, i) in getNotiList" :key="i" class="nMetaWrapper">
        <div class="nMetasBox">
          <img
            :src="showProfile(item.inviter_img.profile_img)"
            alt="userProfile"
            class="nImage"
          />
          <p>{{ item.inviter }}님의 초대 알림</p>
        </div>
        <div class="nNewBtn">
          <div @click="accept(item)" class="nExpandBtn">
            <v-icon small>mdi-charity</v-icon><p>수락</p>
          </div>
          <div @click="reject(item)" class="nExpandBtn">
            <v-icon small>mdi-account-off</v-icon><p>거절</p>
          </div>
        </div>
      </div>
    </div>
    <div v-else class="nContentBox">
      <img class="nNoneNotiImg" :src="noticeImg" alt="">
      <p class="nNoneNoti">
        새로운 알림이 없습니다.
      </p>
    </div>
    <Nav />
  </div>
</template>

<script>
import router from "@/router";
import Nav from "../nav/Nav.vue";
import { mapGetters, mapMutations, mapActions } from "vuex";

export default {
  name: "Notification",
  components: {
    Nav
  },
  data() {
    return {
      wHeight: 0,
      wWidth: 0,
      noticeImg: "https://image.flaticon.com/icons/png/512/2361/2361863.png"
    };
  },
  methods: {
    ...mapActions(["bringNotice", "joinChan", "rejectInvite"]),
    ...mapMutations(["setChanId"]),
    async accept(item) {
      await this.joinChan(item);
      this.bringNotice();
    },
    async reject(item) {
      await this.rejectInvite(item);
      this.bringNotice();
    },
    goHome() {
      router.push("/")
    },
    showProfile(profile_img) {
      return profile_img
        ? this.profileAddr + profile_img
        : require("../../assets/basic_userImage.png");
    },
  },
  computed: {
    ...mapGetters(["isLoggedIn", "getNotiList"])
  },
  async created() {
    if (!this.isLoggedIn) {
      router.push("/login");
    } else {
      await this.bringNotice();
      console.log(this.getNotiList)
    }
  }
};
</script>

<style scoped src="./notification.css"></style>
