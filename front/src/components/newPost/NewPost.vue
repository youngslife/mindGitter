<template>
  <v-container>
    <v-row>
      <v-col cols="2"
        ><v-icon class="back" @click="goHome">fas fa-arrow-left</v-icon></v-col
      >
      <v-col cols="10" class="diaryName"><h1>일기장1</h1></v-col>
      <!-- <v-col cols="2"
        ><v-icon class="back" @click="goHome">fas fa-arrow-left</v-icon></v-col
      > -->
    </v-row>
    <form class="AddPostForm" @submit.prevent="addPost(postInfo)">
      <div class="AddPostForm">
        <ul id="posttitle">
          <label for="posttitle">Title</label
          ><br />
          <input
            v-model="postInfo.title"
            type="text"
            id="posttitle"
            placeholder="제목"
          />
        </ul>
        <ul id="postvideo">
          <label for="postvideo">Video</label
          ><br />
          <input type="file" id="postvideo" @change="onFileChange" />
          <div class="preview">
            영상 사진
          </div>
        </ul>
        <ul id="posttag">
          <label for="posttag">Tags</label
          ><br />
          <input
            v-model="postInfo.tags"
            type="text"
            id="posttag"
            placeholder="관련 태그"
          />
        </ul>
        <ul id="postposs">
          <input type="checkbox" id="postposs" v-model="postInfo.possible" />
          <label for="postposs">Comment 허용</label>
        </ul>
        <ul id="saveVideo">
          <input type="checkbox" id="saveVideo" v-model="postInfo.saveVideo" />
          <label for="saveVideo">영상 저장</label>
        </ul>
        <button class="submit">Upload</button>
      </div>
    </form>
  </v-container>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
import router from "@/router";
// import AWS from "aws-sdk";

export default {
  name: "createDiary",
  data() {
    return {
      postInfo: {
        title: null,
        video: null,
        tags: null,
        possible: false,
        saveVideo: false,
        file: null,
        fileName: null
      }
    };
  },
  methods: {
    ...mapActions(["addPost"]),
    goHome() {
      router.push("/");
    },
    async onFileChange(e) {
      const files = e.target.files;
      if (files) {
        this.postInfo.file = files[0];
        this.postInfo.fileName = String(this.getUserId) + new Date().getTime();
      }
    }
  },
  computed: {
    ...mapGetters(["getUserId"])
  }
};
</script>

<style src="./NewPost.css" scoped></style>
