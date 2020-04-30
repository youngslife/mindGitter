<template>
  <v-container class="hContainer">
    <h1>notification</h1>
    <div v-if="getNotiList">
      <div v-if="getNotiList.length">
        <div v-for="(item, i) in getNotiList" :key="i" class="notification">
          <v-row class="inviter">
            <v-col>
              {{ item.inviter }}
            </v-col>
            <v-col>
              <v-row>
                <v-btn @click="accept(item)">
                  수락
                </v-btn>
                <v-btn @click="reject(item)">
                  거절
                </v-btn>
              </v-row>
            </v-col>
          </v-row>
        </div>
      </div>
      <div v-else>
        새로운 알림이 없습니다.
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
