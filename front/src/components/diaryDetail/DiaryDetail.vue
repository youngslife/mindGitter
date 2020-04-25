<template>
  <div class="dairyDetail">
    <v-icon class="back" @click="goPostList">fas fa-arrow-left</v-icon>
    <h1>{{ getSelectedChan.title }}</h1>
    <div class="video" v-for="(video, i) in videos" :key="i">
      <video width="100%" height="100%" controls class="dvideo">
        <source :src="selectedDiary.video_file" :type="video.type" />
      </video>
    </div>
    <div class="temp"></div>
    <v-tabs fixed-tabs>
      <v-tab v-for="mode in modes" :key="mode" @click="changeMode(mode)">{{
        mode
      }}</v-tab>
    </v-tabs>
    <div class="text" v-if="selectedMode == 'Detail'">
      <h3>{{ selectedDiary.title }}</h3>
      <div class="tags">
        <span v-for="(tag, idx) in selectedDiary.tags" :key="idx"
          >#{{ tag }} </span
        >
      </div>
      <div class="context">
        {{ selectedDiary.context }}
      </div>
      <!-- <div class="additionalInfo">
        <span>작성자: {{ getWriterInfo.username }}</span>
        <br />
        <span>작성시간: {{ `${selectedDiary.created_at.slice(0, 10)}  ${selectedDiary.created_at.slice(11, 16)}` }}</span>
      </div> -->
    </div>
    <div class="text" v-if="selectedMode == 'Analysis'">
      <span>{{ selectedMode }}</span>
    </div>
    <div class="text" v-if="selectedMode == 'Comment'">
      <span>{{ selectedMode }}</span>
    </div>
    <div class="additionalInfo">
      <span>작성자: {{ getWriterInfo.username }}</span>
      <br />
      <span>작성시간: {{ `${selectedDiary.created_at.slice(0, 10)}  ${selectedDiary.created_at.slice(11, 16)}` }}</span>
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
      videoURL:
        "https://mind-gitter-diary.s3.ap-northeast-2.amazonaws.com/diary/diary.mp4",
      videos: [
        {
          name: require("../../assets/test/Clouds.mp4"),
          type: "video/mp4"
        }
      ],
      writer: null
    };
  },
  computed: {
    ...mapGetters(["getSelectedChan", "getSelectedDiary", "getWriterInfo"])
  },
  methods: {
    goPostList() {
      router.push("/postList");
    },
    changeMode(mode) {
      this.selectedMode = mode;
    }
  },
  created() {
    this.selectedDiary = this.getSelectedDiary;
    console.log(this.selectedDiary.video_file)
    // console.log(this.selectedDiary)
    // console.log(this.getSelectedChan)
  }
};
</script>

<style src="./DiaryDetail.css" scoped></style>
