<template>
  <div class="userDetail">
    <div class="userId">
      <p>
        {{ getUserName }}
      </p>
      <button class="settings">
        <v-icon>fas fa-cog</v-icon>
      </button>
    </div>
    <img
      class="userprofile"
      src="../../assets/userprofile.jpg"
      alt="userprofile"
    />
    <Nav />
  </div>
</template>

<script>
import Nav from "../nav/Nav.vue";
import { mapGetters } from "vuex";

export default {
  name: "UserDetail",
  components: {
    Nav
  },
  computed: {
    ...mapGetters(["getUserName"])
  }
};
</script>

<style src="./UserDetail.css" scoped></style>
