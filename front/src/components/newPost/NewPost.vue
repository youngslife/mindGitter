<template>
  <v-container>
    <v-row>
      <v-col cols="10" class="diaryName"><h1>일기장1</h1></v-col>
      <v-col cols="2"
        ><v-icon class="back" @click="goHome">fas fa-arrow-left</v-icon></v-col
      >
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
        <button class="submit" @click="uploadDiary">Upload</button>
      </div>
    </form>
  </v-container>
</template>

<script>

import { mapActions } from "vuex";
import router from "@/router";
import AWS from "aws-sdk";

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
      },
      rawVideo: null,
      //s3setting
      albumBucketName: process.env.VUE_APP_BUCKET_NAME,
      bucketRegion: process.env.VUE_APP_BUCKET_REGION,
      IdentifyPool: process.env.VUE_APP_IDENTIFYPOOL,
      s3: {},
    };
  },
  async mounted() {
    this.s3Init()
  },
  methods: {
    ...mapActions(["addPost"]),
    goHome() {
      router.push("/");
    },
    s3Init() {
      AWS.config.update({
        region: this.bucketRegion,
        credentials: new AWS.CognitoIdentityCredentials({
          IdentityPoolId: this.IdentifyPool
        })
      });

      this.s3 = new AWS.S3({
        apiVersion: "2006-03-01",
        params: { Bucket: this.albumBucketName }
      });
    },
    s3upload(fileName) {
      console.log('s3upload')
      this.postInfo.video = fileName
      return this.s3
        .upload({
          Key: fileName,
          Body: this.rawVideo,
          ACL: "public-read-write"
        })
        .promise();
    },
    async onFileChange(e) {
      const files = e.target.files;
      if (files) {
        console.log(files);
        this.rawVideo = files[0];
      }
    },
    async uploadDiary() {
      try{
        let res = await this.s3upload('test.mp4')
      } catch {
        alert("s3에 업로드 하는 중 에러가 발생했습니다.")
      }
    }
  },
};
</script>

<style src="./NewPost.css" scoped></style>
