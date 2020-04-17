<template>
  <v-container class="hContainer">
    <v-carousel
      :show-arrows="carOption"
      hide-delimiter-background
      delimiter-icon="mdi-minus"
      light
      height="98vh"
    >
      <v-carousel-item v-for="(item, i) in diaryList" :key="i">
        <h1>{{ item.title }}</h1>
        <v-img :src="item.src" alt="No Image" class="cImage"></v-img>
        <div class="cSummary">
          <h2>Summary of Diary</h2>
          <p>{{ item.content }}</p>
        </div>
        <button @click="goDetail" class="cBtn">Detail</button>
      </v-carousel-item>
      <v-carousel-item>
        <h1>새 일기장</h1>
        <div class="aCon">
          <v-icon class="newBtn" @click="goCreate">mdi-plus</v-icon>
        </div>
      </v-carousel-item>
    </v-carousel>
  </v-container>
</template>

<script>
import router from "@/router";
import { mapGetters } from "vuex";

export default {
  name: "Home",
  data() {
    return {
      wHeight: 0,
      wWidth: 0,
      carOption: false,
      diaryList: [],
      addImg:
        "https://w0.pngwave.com/png/106/279/computer-icons-medicine-health-care-plus-button-png-clip-art.png"
    };
  },
  methods: {
    // 유저의 일기 목록 가져오기
    getDiary() {
      const gotList = [
        {
          title: "첫 번째",
          content: "첫 번째 일기의 내용입니다",
          src: "https://cdn.vuetifyjs.com/images/carousel/squirrel.jpg"
        },
        {
          title: "두 번째",
          content: "두 번째 일기의 내용입니다",
          src: "https://cdn.vuetifyjs.com/images/carousel/sky.jpg"
        },
        {
          title: "세 번째",
          content: "세 번째 일기의 내용입니다",
          src: "https://cdn.vuetifyjs.com/images/carousel/bird.jpg"
        },
        {
          title: "네 번째",
          content: "네 번째 일기의 내용입니다",
          src: "https://cdn.vuetifyjs.com/images/carousel/planet.jpg"
        }
      ];
      this.diaryList = gotList;
    },
    goCreate() {
      router.push("createDiary");
    },
    goDetail() {
      router.push("diaryList");
    }
  },
  // vuex Login 연동
  computed: {
    ...mapGetters(["isLoggedIn"])
  },
  created() {
    if (this.isLoggedIn) {
      this.getDiary();
    } else {
      router.push("/login");
    }
  }
};
</script>

<style scoped src="./home.css"></style>
