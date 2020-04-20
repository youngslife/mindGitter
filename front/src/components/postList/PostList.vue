<template>
  <div class="diaryList">
    <h1>Diary Name</h1>
    <div class="posts">
      
    </div>
    <Nav />
  </div>
</template>

<script>
import Nav from "../nav/Nav.vue";

export default {
  name: "DiaryList",
  components: {
    Nav
  }
};
</script>

<style src="./PostList.css" scoped></style>
