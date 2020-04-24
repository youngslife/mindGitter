<template>
  <div class="dairyDetail">
    <v-icon class="back" @click="goPostList">fas fa-arrow-left</v-icon>
    <h1>{{ getSelectedChan }}</h1>
    <div class="video" v-for="(video, i) in videos" :key="i">
      <video width="100%" height="100%" controls class="dvideo">
        <source :src="videoURL" :type="video.type" />
      </video>
    </div>
    <div class="temp"></div>
    <v-tabs fixed-tabs>
      <v-tab v-for="mode in modes" :key="mode" @click="changeMode(mode)">{{
        mode
      }}</v-tab>
    </v-tabs>
    <div class="text">
      <h3>{{ selectedDiary.title }}</h3>
      <span>{{ selectedDiary.tags }}</span>
      <br />
      <span>{{ selectedMode }}</span>
    </div>
  </div>
</template>

<script>
import router from "@/router";
import { mapGetters } from "vuex";

export default {
  name: "DiaryDetail",
  data() {
    return {
      modes: ["Detail", "Analysis", "Comment"],
      selectedMode: "Detail",
      selectedDiary: "",
      videoURL: "https://mind-gitter-diary.s3.ap-northeast-2.amazonaws.com/diary/diary.mp4",
      videos: [
        {
          name: require("../../assets/test/Clouds.mp4"),
          type: "video/mp4",
        },
      ],
    };
  },
  computed: {
    ...mapGetters(["getSelectedChan", "getSelectedDiary"]),
  },
  methods: {
    goPostList() {
      router.push("/postList");
    },
    changeMode(mode) {
      this.selectedMode = mode;
    },
  },
  created() {
    this.selectedDiary = this.getSelectedDiary;
  },
};
</script>

<style src="./DiaryDetail.css" scoped></style>
