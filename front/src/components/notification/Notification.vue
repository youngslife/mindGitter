<template>
  <div class="ddContainer">
    <div class="ddBar">
      <div class="ddBtn ddBackBtn" @click="goHome">
        <v-icon color="rgba(0, 0, 0, 0.5)" small>fas fa-arrow-left</v-icon>
      </div>
      <p class="ddDate">Noti</p>
    </div>
    <div v-if="getNotiList && getNotiList.length" class="hContentBox">
      <div v-for="(item, i) in getNotiList" :key="i" class="hMetaWrapper">
        <div class="hMetasBox">
          {{ item.inviter }}
        </div>
        <div class="hNewBtn">
          <div @click="accept(item)" class="ddExpandBtn">
            <p>공유</p>
          </div>
          <div @click="reject(item)" class="ddExpandBtn">
            <p>거절</p>
          </div>
        </div>
      </div>
    </div>
    <div v-else class="hContentBox">
      <p>
        새로운 알림이 없습니다.
      </p>
    </div>
    <Nav />
  </div>
</template>

<script>
import router from "@/router";
import Nav from "../nav/Nav.vue";
import { mapGetters, mapMutations, mapActions } from "vuex";

export default {
  name: "Notification",
  components: {
    Nav
  },
  data() {
    return {
      wHeight: 0,
      wWidth: 0
    };
  },
  methods: {
    ...mapActions(["bringNotice", "joinChan", "rejectInvite"]),
    ...mapMutations(["setChanId"]),
    async accept(item) {
      // console.log(item)
      await this.joinChan(item);
      this.bringNotice();
    },
    async reject(item) {
      await this.rejectInvite(item);
      this.bringNotice();
    },
    goHome() {
      router.push("/")
    }
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
