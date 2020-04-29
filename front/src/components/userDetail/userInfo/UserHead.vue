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
      <button class="settings" @click="setUserInfoModal(true)">
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
    ...mapGetters(["getUserName", "isLoggedIn"])
  },
  methods: {
    ...mapMutations(["setUserImgModal", "setUserInfoModal"])
  }
};
</script>

<style></style>
