<template>
  <div class="dairyDetail">
    <v-icon class="back" @click="goPostList">fas fa-arrow-left</v-icon>
    <h1>{{ getSelectedChan }}</h1>
    <div class="video">
      <!-- <my-video :sources="video.sources" :options="video.options"></my-video> -->
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

// import myVideo from "vue-video";

export default {
  name: "DiaryDetail",
  data() {
    return {
      modes: ["Detail", "Analysis", "Comment"],
      selectedMode: "Detail",
      selectedDiary: "",
      video: {
        sources: [
          {
            src: "../assets/test.mp4",
            type: "video/mp4"
          }
        ],
        options: {
          autoplay: true,
          volume: 0.6
          // poster: "https://www.youtube.com/watch?v=1C7IXEejZeU"
        }
      }
    };
  },
  components: {
    // myVideo
  },
  computed: {
    ...mapGetters(["getSelectedChan", "getSelectedDiary"])
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
  }
};
</script>

<style src="./DiaryDetail.css" scoped></style>
