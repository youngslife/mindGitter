<template>
  <div class="createDiary">
    <v-icon class="back" @click="goHome">fas fa-arrow-left</v-icon>
    <form class="AddDiaryForm" @submit.prevent="addChannel(PostInfo)">
      <div class="AddDiaryForm">
        <h1>Add Diary</h1>
        <ul id="diarytitle">
          <label for="diarytitle">Diary Title</label
          ><br />
          <input
            v-model="PostInfo.title"
            type="text"
            id="diarytitle"
            placeholder="제목"
          />
        </ul>
        <ul id="diarydescription">
          <label for="diarydescription">Description</label
          ><br />
          <input
            v-model="PostInfo.description"
            type="text"
            id="diarydescription"
            placeholder="다이어리 설명"
          />
        </ul>
        <ul id="diaryimage">
          <label for="diaryimage">Image</label
          ><br />
          <input type="file" id="diaryimage" @change="onFileChange" />
        </ul>
        <button class="submit">만들기</button>
      </div>
    </form>
  </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
import router from "@/router";

export default {
  name: "createDiary",
  data() {
    return {
      PostInfo: {
        title: null,
        description: null,
        file: null,
        fileName: null
      }
    };
  },
  computed: {
    ...mapGetters(["getUserId"])
  },
  methods: {
    ...mapActions(["addChannel"]),
    onFileChange(e) {
      const files = e.target.files;
      if (files) {
        this.PostInfo.file = files[0];
        this.PostInfo.fileName =
          String(this.getUserId) + new Date().getTime() + ".jpg";
      }
    },
    goHome() {
      router.push("/");
    }
  }
};
</script>

<style src="./createDiary.css" scoped></style>
