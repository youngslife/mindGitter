<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script>

export default {
  created() {
    this.$store.dispatch("initialLogin");
  }
};
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Jua&display=swap');
#app {
  font-family: 'Jua', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>
