<template>
  <v-row>
    <v-col cols="3">
      <img
        class="userProfile"
        src="../../../assets/basic_userImage.png"
        alt="userprofile"
        @click="setUserImgModal(true)"
      />
    </v-col>
    <v-col class="userSummary" cols="9">
      <v-row>
        <v-col cols="4">Total</v-col>
        <v-col cols="4">Create</v-col>
        <v-col cols="4">Diary</v-col>
      </v-row>
    </v-col>
  </v-row>
</template>

<script>
import { mapMutations } from "vuex";

export default {
  methods: {
    ...mapMutations(["setUserImgModal"])
  }
};
</script>

<style src="./UserInfo.css" scoped></style>
