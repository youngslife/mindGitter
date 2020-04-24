<template>
  <div class="Nav">
    <v-bottom-navigation :value="activeBtn" grow fixed height="40px">
      <v-btn @click="goHome">
        <v-icon>fas fa-home</v-icon>
      </v-btn>

      <v-btn @click="goCreateDiary">
        <v-icon>fas fa-plus</v-icon>
      </v-btn>

      <v-btn @click="goUserDetail">
        <v-icon>fas fa-align-justify</v-icon>
      </v-btn>
    </v-bottom-navigation>
  </div>
</template>

<script>
import router from "@/router";

export default {
  name: "Nav",
  data() {
    return {
      activeBtn: 1
    };
  },
  methods: {
    goHome() {
      router.push("/");
    },
    goCreateDiary() {
      router.push("newPost");
    },
    goUserDetail() {
      router.push("userDetail");
    }
  }
};
</script>

<style></style>
