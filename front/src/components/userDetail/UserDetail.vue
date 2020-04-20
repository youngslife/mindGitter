<template>
  <div class="userDetail">
    <div class="userId">
      <p v-if="isLoggedIn">
        {{ getUserName }}
      </p>
      <button class="settings" @click.prevent="logout">
        <v-icon>fas fa-sign-out-alt</v-icon>
      </button>
    </div>
    <img
      class="userprofile"
      src="../../assets/userprofile.jpg"
      alt="userprofile"
    />
    <div class="totalInfo">
      <v-row>
        <v-col>
          First
        </v-col>
        <v-col>
          Total
        </v-col>
        <v-col>
          Channel
        </v-col>
      </v-row>
      무슨 정보를 넣으면 좋겠다
    </div>
    <div class="emotion">
      <h3>Emotion</h3>
      <div class="emotionDetail">
        감정 분석 결과
      </div>
    </div>
    <div class="tag">
      <h3>Tag</h3>
      <div class="tagDetail">
        tag 분석 결과
      </div>
    </div>
    <Nav />
  </div>
</template>

<script>
import Nav from "../nav/Nav.vue";
import { mapGetters, mapActions } from "vuex";

export default {
  name: "UserDetail",
  components: {
    Nav
  },
  computed: {
    ...mapGetters(["getUserName", "isLoggedIn"])
  },
  methods: {
    ...mapActions(["logout"])
  }
};
</script>

<style src="./UserDetail.css" scoped></style>
