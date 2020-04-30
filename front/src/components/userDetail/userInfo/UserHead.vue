<template>
  <v-row>
    <v-col cols="10" class="userName">
      <div v-if="getUserName">
        {{ getUserName }}
      </div>
      <div v-else>
        <p>로그인을 안하셨군요?</p>
      </div>
    </v-col>
    <v-col cols="2" class="outBtn">
      <button class="settings" @click="changeModal">
        <v-icon>fas fa-cog</v-icon>
      </button>
    </v-col>
  </v-row>
</template>

<script>
import { mapGetters, mapMutations } from "vuex";

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
    }
  }
};
</script>

<style></style>
