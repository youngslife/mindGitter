<template>
  <div class="commentContainer">
    <div class="reviewForm">
      <div class="userName">
        <p>user</p>
      </div>
      <div class="reviewInput">
        <input type="text" class="context" v-model="context" />
      </div>
      <div class="btn">
          <button class="reviewBtn" @click.prevent="addComment(context)">등록</button>
      </div>
    </div>
    <hr class="partialLine" />
    <div class="Reviews">
        <div class="review" v-for="(comment, i) in commentList" :key="i">
            <div class="userName">{{ comment.username }}</div>
            <div class="context">{{ comment.context }}</div>
            <div class="btn">
                <button class="delBtn">DEL</button>
            </div>
        </div>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex";

export default {
  name: "newComment",
  data() {
    return {
        context: null,
        commentList: Array,
        channelInfo: Object
    };
  },
  methods: {
      ...mapActions(["addComment"])
  },
  computed: {
      ...mapGetters(["getSelectedDiary", "getUserName", "getSelectedChan"])
  },
  created() {
      this.commentList = this.getSelectedDiary.comment_set
      this.channelInfo = this.getSelectedChan
      this.commentList.forEach(comment => {
        this.channelInfo.user_set.forEach(userinfo => {
            if (comment.user == userinfo.id) {
                comment["username"] = userinfo.username
                console.log(comment)
            }
        })
      })
  }
};
</script>

<style src="./Comments.css" scoped></style>
