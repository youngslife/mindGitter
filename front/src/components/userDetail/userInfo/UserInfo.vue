<template>
  <v-row>
    <v-col cols="3">
      <img class="userProfile" :src="showProfile()" alt="userprofile" />
    </v-col>
    <v-col class="userSummary" cols="9">
      <v-row>
        <v-col cols="4">Total</v-col>
        <v-col cols="4">Create</v-col>
        <v-col cols="4">Diary</v-col>
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
    ...mapActions(["bringUserProfile"]),
    showProfile() {
      return this.getUserProfile
        ? this.profileAddr + this.getUserProfile
        : require("../../../assets/basic_userImage.png");
    }
  },
  computed: {
    ...mapGetters(["getUserProfile"])
  },
  async created() {
    await this.bringUserProfile();
  }
};
</script>

<style src="./UserInfo.css" scoped></style>
