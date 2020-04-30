<template>
  <v-row v-if="getUserInfoSet && getChanList">
    <v-col cols="3">
      <img class="userProfile" :src="showProfile()" alt="userprofile" />
    </v-col>
    <v-col class="userSummary" cols="9">
      <v-row>
        <v-col cols="4">Post</v-col>
        <v-col cols="5">First Post</v-col>
        <v-col cols="3">Diary</v-col>
      </v-row>
      <v-row>
        <v-col cols="4">총 {{ getUserInfoSet.post_set.length }}편</v-col>
        <v-col cols="5" v-if="getUserInfoSet.post_set.length">{{
          getUserInfoSet.post_set[
            getUserInfoSet.post_set.length - 1
          ].created_at.slice(0, 10)
        }}</v-col>
        <v-col cols="5" v-else>
          -
        </v-col>
        <v-col cols="3">{{ getChanList.length }}개</v-col>
      </v-row>
    </v-col>
  </v-row>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
// src="../../../assets/basic_userImage.png"
export default {
  data() {
    return {
      profileAddr: process.env.VUE_APP_STATIC_ADDR + "profile/"
    };
  },
  methods: {
    ...mapActions(["bringUserProfile", "bringUserInfoSet", "bringChanList"]),
    showProfile() {
      return this.getUserProfile
        ? this.profileAddr + this.getUserProfile
        : require("../../../assets/basic_userImage.png");
    }
  },
  computed: {
    ...mapGetters(["getUserProfile", "getUserInfoSet", "getChanList"])
  },
  async created() {
    await this.bringUserProfile();
    await this.bringUserInfoSet();
    await this.bringChanList();
  }
};
</script>

<style src="./UserInfo.css" scoped></style>
