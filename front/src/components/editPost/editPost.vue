<template>
  <div class="createPost">
    <div class="createPostHeader">
      <v-row>
        <v-col cols="2"><v-icon class="back" @click="goList">
          fas fa-arrow-left</v-icon></v-col>
        <v-col cols="10" class="diaryName"></v-col>
      </v-row>
      <div>
        <h2>{{ getChanName }}</h2>
      </div>
    </div>
    <form class="AddPostForm" @submit.prevent="editPost(postInfo)">
      <div class="AddPostForm">
          <v-text-field
            v-model="postInfo.title"
            type="text"
            id="posttitle"
            placeholder="title"
          ></v-text-field>
          <v-file-input prepend-icon="" append-outer-icon="mdi-camera" accept="video/*" id="postvideo" placeholder="upload your video" @change="onFileChange"></v-file-input>
          <video
            class="videoPreview"
            :src="videoTempUrl"
            controls="controls"
          />
          <v-text-field
            v-model="postInfo.tags"
            type="text"
            id="posttag"
            placeholder="tags"
          ></v-text-field>
          <input type="checkbox" id="postposs" v-model="postInfo.possible" />
          <label class="optCheck" for="postposs">Accept comments</label>
        <ul id="saveVideo">
          <input type="checkbox" id="saveVideo" v-model="postInfo.saveVideo" />
          <label class="optCheck" for="saveVideo">Save video</label>
        </ul>
        <button class="submit">Upload</button>
      </div>
    </form>
    <v-card class="loading" v-if="getPostLoading">
      ...영상을 모델로 넘기고 있습니다...<br />
      조금만 기다려 주세요.<br />
      <v-progress-circular indeterminate color="green"></v-progress-circular>
    </v-card>
  </div>
</template>

<script>
import { mapGetters, mapMutations, mapActions } from "vuex";
import router from "@/router";

export default {
  name: "createDiary",
  data() {
    return {
      postInfo: {
        title: null,
        tags: null,
        context: "context",
        cover_image: "cover_image",
        possible: false,
        saveVideo: false,
        file: null,
        fileName: null
      },
      videoAddr: process.env.VUE_APP_STATIC_ADDR + "diary/",
      videoTempUrl: null
    };
  },
  methods: {
    ...mapActions(["editPost"]),
    ...mapMutations(["setChanName", "setChanId"]),
    goList() {
      router.push("/postList");
    },
    async onFileChange(e) {
      const file = e;
      if (file) {
        // const file = files[0];
        this.postInfo.file = file;
        this.postInfo.fileName =
          String(this.getUserId) + new Date().getTime() + ".mp4";
        const blobFile = new Blob([file], { type: file.type });
        // console.log(blobFile)
        this.videoTempUrl = URL.createObjectURL(blobFile);
      } else {
        this.postInfo.fileName = '';
        this.videoTempUrl = '';
      }
    }
  },
  computed: {
    ...mapGetters(["getUserId", "getChanName", "getPostLoading", "getEditDiary"])
  },
  async created() {
    const chanName = sessionStorage.getItem("chanName");
    const chanId = sessionStorage.getItem("chan");
    if (chanId) {
      this.setChanName(chanName);
      this.setChanId(chanId);
    } else {
      router.push("/");
    }
    if (this.getEditDiary) {
      this.postInfo.title = this.getEditDiary.title;
      this.postInfo.tags = this.getEditDiary.tags;
      this.postInfo.possible = this.getEditDiary.is_use_comment;
      this.postInfo.saveVideo = this.getEditDiary.is_save_video;
      this.videoTempUrl = this.videoAddr + this.getEditDiary.video_file;
      console.log(this.videoAddr + this.getEditDiary.video_file)
      this.postInfo.fileName = this.getEditDiary.video_file;
      this.postInfo.post_id = this.getEditDiary.pk;
    } else {
      router.push("/postList");
    }
  }
};
</script>

<style src="./editPost.css" scoped></style>
