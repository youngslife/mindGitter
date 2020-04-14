<template>
  <v-row>
    <v-carousel :show-arrows="carOption">
      <v-carousel-item v-for="(item, i) in diaryList" :key="i" :src="item.src">
      </v-carousel-item>
      <v-carousel-item :src="addImg">
        <button @click="goCreate">Add Diary</button>
      </v-carousel-item>
    </v-carousel>
  </v-row>
</template>

<script>
import router from "@/router";
// import { mapGetters } from "vuex";
export default {
  data() {
    return {
      carOption: false,
      diaryList: [],
      addImg: "https://cdn.vuetifyjs.com/images/carousel/squirrel.jpg",
      isLoggedIn: true
    };
  },
  methods: {
    // 유저의 일기 목록 가져오기
    getDiary() {
      const gotList = [
        {
          src: "https://cdn.vuetifyjs.com/images/carousel/squirrel.jpg"
        },
        {
          src: "https://cdn.vuetifyjs.com/images/carousel/sky.jpg"
        },
        {
          src: "https://cdn.vuetifyjs.com/images/carousel/bird.jpg"
        },
        {
          src: "https://cdn.vuetifyjs.com/images/carousel/planet.jpg"
        }
      ];
      this.diaryList = gotList;
    },
    goCreate() {
      router.push("createDiary");
    }
  },
  // // vuex Login 연동
  // computed: {
  //   ...mapGetters(["isLoggedIn"])
  // },
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
