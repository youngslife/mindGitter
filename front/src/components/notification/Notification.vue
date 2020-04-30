<template>
  <v-container class="hContainer">
    <h1>notification</h1>
    <div
      v-for="(item, i) in getNotiList" :key="i">
    >
      <div>
      {{item}}
      </div>
    </div>
  </v-container>
</template>

<script>
import router from "@/router";
import { mapGetters, mapMutations, mapActions } from "vuex";

export default {
  name: "Notification",
  data() {
    return {
      wHeight: 0,
      wWidth: 0,
   
    };
  },
  methods: {
    ...mapActions(["bringNotice"]),
    ...mapMutations(["setChanId"]),

  },
  computed: {
    ...mapGetters(["isLoggedIn", "getNotiList"])
  },
  async created() {
    if (!this.isLoggedIn) {
      router.push("/login");
    } else {
      await this.bringNotice();
    }
  }
};
</script>

<style scoped src="./notification.css"></style>