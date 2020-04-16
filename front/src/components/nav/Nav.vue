<template>
  <div class="Nav">
    <v-bottom-navigation :value="activeBtn" grow fixed height="40px">
      <v-btn href="/home">
        <v-icon>fas fa-home</v-icon>
      </v-btn>

      <v-btn href="/createDiary">
        <v-icon>fas fa-plus</v-icon>
      </v-btn>

      <v-btn href="/userDetail">
        <v-icon>fas fa-align-justify</v-icon>
      </v-btn>
    </v-bottom-navigation>
  </div>
</template>

<script>
export default {
  name: "Nav",
  data() {
    return {
      activeBtn: 1
    };
  }
};
</script>

<style></style>
