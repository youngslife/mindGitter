<template>
  <v-container class="hContainer">
    <v-carousel
      v-if="getChanList"
      :show-arrows="carOption"
      hide-delimiter-background
      delimiter-icon="mdi-minus"
      light
      height="98vh"
    >
      <template>
        <v-btn @click="goUserDetail" class="userPageBtn" fab small absolute>
          <v-icon>mdi-account-circle</v-icon>
        </v-btn>
      </template>
      <v-carousel-item v-for="(item, i) in getChanList" :key="i">
        <h1>{{ item.title }}</h1>
        <v-img
          :src="imgAddr + item.cover_image"
          alt="No Image"
          class="cImage"
        ></v-img>
        <div class="cSummary">
          <h2>Summary of Diary</h2>
          <p>{{ item.description }}</p>
        </div>
        <button @click="goDetail(item.id)" class="cBtn">Detail</button>
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
import { mapGetters, mapMutations, mapActions } from "vuex";

export default {
  name: "Home",
  data() {
    return {
      wHeight: 0,
      wWidth: 0,
      imgAddr: process.env.VUE_APP_STATIC_ADDR + "channel/",
      carOption: false,
      addImg:
        "https://w0.pngwave.com/png/106/279/computer-icons-medicine-health-care-plus-button-png-clip-art.png"
    };
  },
  methods: {
    ...mapActions(["bringChanList"]),
    ...mapMutations(["setChanId"]),
    goCreate() {
      router.push("createDiary");
    },
    //은영추가
    goUserDetail() {
      router.push("userDetail");
    },
    async goDetail(channelId) {
      await this.setChanId(channelId);
      router.push("/postList");
    }
  },
  computed: {
    ...mapGetters(["isLoggedIn", "getChanList"])
  },
  async created() {
    if (!this.isLoggedIn) {
      router.push("/login");
    } else {
      await this.bringChanList();
    }
  }
};
</script>

<style scoped src="./home.css"></style>
