<template>
  <div class="commentContainer" v-if="currentUser">
    <v-row class="reviewForm">
      <v-col cols="2" class="userImage">
        <img
          :src="showProfile(currentUser.profile_img)"
          alt="userProfile"
          class="uImage"
        />
      </v-col>
      <v-col class="reviewInput">
        <input type="text" class="context" v-model="context" placeholder="댓글 입력 .."/>
      </v-col>
      <v-col cols="2" class="btn">
        <button class="reviewBtn" @click.prevent="addComment(context)">
          게시
        </button>
      </v-col>
    </v-row>
    <!-- <hr class="partialLine" /> -->
    <div class="Reviews">
      <div
        class="review"
        v-for="(comment, i) in getSelectedDiary.comment_set"
        :key="i"
      >
        <Comment :comment="comment" />
      </div>
    </div>
  </div>
</template>

<script>
import { mapMutations, mapGetters, mapActions } from "vuex";
import axios from "axios";
import Comment from "./comment/Comment.vue";
import router from "@/router";

export default {
  components: {
    Comment,
  },
  data() {
    return {
      context: null,
      profileAddr: process.env.VUE_APP_STATIC_ADDR + "profile/",
      currentUser: null,
    };
  },
  methods: {
    ...mapActions(["addComment"]),
    ...mapMutations(["setUserName"]),
    showProfile(profile_img) {
      return profile_img
        ? this.profileAddr + profile_img
        : require("../../../assets/basic_userImage.png");
    },
  },
  computed: {
    ...mapGetters([
      "getSelectedDiary",
      "getUserName",
      "getSelectedChan",
      "getUserId",
    ]),
  },
  async created() {
    const username = sessionStorage.getItem("userName");
    if (username) {
      await this.setUserName(username);
    } else {
      router.push("/");
    }
  },
  async mounted() {
    const token = sessionStorage.getItem("jwt");
    const HOST = process.env.VUE_APP_SERVER_HOST;
    const options = {
      headers: {
        Authorization: "JWT " + token,
      },
    };
    await axios.get(`${HOST}/current_user`, options).then((res) => {
      this.currentUser = res.data;
    });
  },
};
</script>

<style src="./Comments.css" scoped></style>
