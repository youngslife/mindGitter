<template>
  <v-container v-if="getSelectedChan">
    <v-row>
      <v-col cols="2"
        ><v-icon class="back" @click="goList">fas fa-arrow-left</v-icon></v-col
      >
      <v-col cols="10" class="diaryName"
        ><h1>{{ getSelectedChan.title }}</h1></v-col
      >
    </v-row>
    <form class="AddPostForm" @submit.prevent="editPost(postInfo)">
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
            <video
              class="videoPreview"
              :src="videoTempUrl"
              controls="controls"
            />
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

export default {
  name: "editPost",
  data() {
    return {
      postInfo: {
        title: null,
        video: null,
        tags: null,
        context: "context",
        cover_image: "cover_image",
        possible: false,
        saveVideo: false,
        file: null,
        fileName: null,
        post_id: null
      },
      videoAddr: process.env.VUE_APP_STATIC_ADDR + "diary/",
      videoTempUrl: null
    };
  },
  methods: {
    ...mapActions(["editPost"]),
    goList() {
      router.push("/postList");
    },
    async onFileChange(e) {
      const files = e.target.files;
      if (files) {
        const file = files[0];
        this.postInfo.file = file;
        this.postInfo.fileName =
          String(this.getUserId) + new Date().getTime() + ".mp4";
        const blobFile = new Blob([file], { type: file.type });
        this.videoTempUrl = URL.createObjectURL(blobFile);
      }
    }
  },
  computed: {
    ...mapGetters(["getSelectedChan", "getEditDiary"])
  },
  async created() {
    if (this.getEditDiary) {
      this.postInfo.title = this.getEditDiary.title;
      this.postInfo.tags = this.getEditDiary.tags;
      this.postInfo.possible = this.getEditDiary.is_use_comment;
      this.postInfo.saveVideo = this.getEditDiary.is_save_video;
      this.videoTempUrl = this.videoAddr + this.getEditDiary.video_file;
      this.postInfo.fileName = this.getEditDiary.video_file;
      this.postInfo.post_id = this.getEditDiary.pk;
    } else {
      router.push("/postList");
    }
  }
};
</script>

<style src="./editPost.css" scoped></style>
