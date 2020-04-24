<template>
  <div class="dairyDetail">
    <v-icon class="back" @click="goPostList">fas fa-arrow-left</v-icon>
    <h1>{{ getSelectedChan }}</h1>
    <div class="video"></div>
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
      selectedDiary: ""
    };
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
