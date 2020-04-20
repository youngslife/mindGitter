<template>
  <div class="diaryList">
    <div class="infoAndSetting">
      <h1>{{ getSelectedChan }}</h1>
      <v-icon>fas fa-user-plus</v-icon>
    </div>
    <div calss="search">
      <v-icon>fas fa-search</v-icon>
      <input type="text" v-model="searchTag" />
      <div class="sharedImage">
        <img
          class="sharedUserProfile"
          src="../../assets/shareduserprofile.jpg"
          alt="sharedUserProfile"
        />
      </div>
    </div>
    <Nav />
  </div>
</template>

<script>
import Nav from "../nav/Nav.vue";
import { mapGetters } from "vuex";

export default {
  name: "DiaryList",
  data() {
    return {
      searchTag: null,
      sharedUser: "멋찌"
    };
  },
  components: {
    Nav
  },
  computed: {
    ...mapGetters(["getSelectedChan"])
  }
};
</script>

<style src="./DiaryList.css" scoped></style>
