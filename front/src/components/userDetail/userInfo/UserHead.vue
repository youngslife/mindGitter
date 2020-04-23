<template>
  <v-row>
    <v-col cols="10" class="userName">
      <div v-if="isLoggedIn">
        {{ getUserName }}
      </div>
      <div v-else>
        <p>로그인을 안하셨군요?</p>
      </div>
    </v-col>
    <v-col cols="2" class="outBtn">
      <button class="settings" @click.prevent="logout">
        <v-icon>fas fa-sign-out-alt</v-icon>
      </button>
    </v-col>
  </v-row>
</template>

<script>
import { mapGetters, mapActions } from "vuex";

export default {
  name: "UserHead",
  computed: {
    ...mapGetters(["getUserName", "isLoggedIn"])
  },
  methods: {
    ...mapActions(["logout"])
  }
};
</script>

<style></style>
