<template>
  <v-row>
    <v-col cols="2">
      <button class="settings" @click="goBack">
        <v-icon color="rgba(0, 0, 0, 0.5)" small>fas fa-arrow-left</v-icon>
      </button>
    </v-col>
    <v-col cols="8" class="userName">
      마이 페이지
    </v-col>
    <v-col cols="2" class="outBtn">
      <button class="settings" @click="changeModal">
        <v-icon color="rgba(0, 0, 0, 0.5)" small>fas fa-ellipsis-v</v-icon>
      </button>
    </v-col>
  </v-row>
</template>

<script>
import { mapGetters, mapMutations } from "vuex";
import router from '@/router'

export default {
  name: "UserHead",
  computed: {
    ...mapGetters(["getUserName", "isLoggedIn", "getUserImgModal"])
  },
  methods: {
    ...mapMutations(["setUserImgModal", "setUserInfoModal", "setUserImgModal"]),
    async changeModal() {
      if (this.getUserImgModal) {
        await this.setUserImgModal();
      }
      this.setUserInfoModal();
    },
    goBack() {
      router.push("/postList");
    },
  }
};
</script>

<style></style>
