<template>
  <div class="userDetail">
    <div class="userId">
      <p>
        jisunl23
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

export default {
  name: "UserDetail",
  components: {
    Nav
  }
};
</script>

<style src="./UserDetail.css" scoped></style>
