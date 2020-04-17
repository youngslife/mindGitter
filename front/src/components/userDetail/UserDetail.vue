<template>
  <div class="userDetail">
    <img
      class="userprofile"
      src="../../assets/userprofile.jpg"
      alt="userprofile"
    />
    <div class="userId">
      <p>
        jisunl23
      </p>
    </div>
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
