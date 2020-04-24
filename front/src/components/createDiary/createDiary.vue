<template>
  <div class="createDiary">
    <v-icon class="back" @click="goHome">fas fa-arrow-left</v-icon>
    <form class="AddDiaryForm" @submit.prevent="addDiary(diaryInfo)">
      <div class="AddDiaryForm">
        <h1>Add Diary</h1>
        <ul id="diarytitle">
          <label for="diarytitle">Diary Title</label
          ><br />
          <input
            v-model="diaryInfo.title"
            type="text"
            id="diarytitle"
            placeholder="제목"
          />
        </ul>
        <ul id="diarydescription">
          <label for="diarydescription">Description</label
          ><br />
          <input
            v-model="diaryInfo.description"
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
import { mapActions } from "vuex";
import router from "@/router";

export default {
  name: "createDiary",
  data() {
    return {
      diaryInfo: {
        title: null,
        image: null,
        description: null
      }
    };
  },
  methods: {
    ...mapActions(["addDiary"]),
    goHome() {
      router.push("/");
    },
    onFileChange(e) {
      const files = e.target.files;
      if (files) {
        this.diaryInfo.image = files[0];
      }
    }
  }
};
</script>

<style src="./createDiary.css" scoped></style>
