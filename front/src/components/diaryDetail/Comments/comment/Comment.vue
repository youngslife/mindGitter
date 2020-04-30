<template>
  <v-row class="comment" align="center"
      justify="center"  v-if="user">
    <v-col cols="2" class="userImage" :user="user">
      <img
        :src="showProfile(user.profile_img)"
        alt="userProfile"
        class="uImage"
      />
    </v-col>
    <v-col class="commentInfo">
      <p class="username">{{ this.user.username }}</p>
      <p class="context">{{ comment.context }}</p>
    </v-col>
    <v-col cols="2" v-if="comment.user == currentUser" class="delBtn">
      <v-icon @click="deleteComment(comment)">fas fa-trash-alt</v-icon>
    </v-col>
  </v-row>
</template>

<script>
import axios from "axios";
import { mapGetters, mapActions } from "vuex";
export default {
  data() {
    return {
      user: null,
      profileAddr: process.env.VUE_APP_STATIC_ADDR + "profile/",
      currentUser: sessionStorage.getItem("userId"),
    };
  },
  methods: {
    ...mapActions(["deleteComment"]),
    showProfile(profile_img) {
      return profile_img
        ? this.profileAddr + profile_img
        : require("../../../../assets/basic_userImage.png");
    },
  },
  props: {
    comment: Object,
  },
  computed: {
    ...mapGetters(["getUserId"]),
  },
  async mounted() {
    const token = sessionStorage.getItem("jwt");
    const HOST = process.env.VUE_APP_SERVER_HOST;
    const options = {
      headers: {
        Authorization: "JWT " + token,
      },
    };
    await axios
      .get(`${HOST}/user/${this.comment.user}`, options)
      .then((res) => {
        this.user = res.data;
      });
  },
};
</script>

<style src="./Comment.css" scoped></style>
