<template>
  <div class="commentContainer">
    <div class="reviewForm">
      <div class="userName">
        {{ getUserName }}
      </div>
      <div class="reviewInput">
        <input type="text" class="context" v-model="context" />
      </div>
      <div class="btn">
        <button class="reviewBtn" @click.prevent="addComment(context)">
          등록
        </button>
      </div>
    </div>
    <hr class="partialLine" />
    <div class="Reviews">
      <div
        class="review"
        v-for="(comment, i) in getSelectedDiary.comment_set"
        :key="i"
      >
        <UserName :userpk="comment.user" />
        <div class="context">{{ comment.context }}</div>
        <div class="btn" v-if="comment.user == getUserId">
          <button class="delBtn" @click="deleteComment(comment)">DEL</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapMutations, mapActions } from "vuex";
import UserName from "./userName/UserName.vue";
import router from "@/router";

export default {
  name: "newComment",
  components: {
    UserName
  },
  data() {
    return {
      context: null,
      commentList: Array,
      channelInfo: Object
    };
  },
  methods: {
    ...mapActions(["addComment", "deleteComment"]),
    ...mapMutations(["setUserName"])
  },
  computed: {
    ...mapGetters(["getSelectedDiary", "getUserName", "getSelectedChan", "getUserId"])
  },
  async created() {
    const username = sessionStorage.getItem("userName");
    if (username) {
      await this.setUserName(username);
    } else {
      router.push("/");
    }
  }
};
</script>

<style src="./Comments.css" scoped></style>
