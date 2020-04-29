<template>
  <v-container class="hnContainer">
    <div class="hnDiary">
      <v-card dark style="border-radius:17px">
        <v-img
          src="../../assets/create.jpg"
          gradient="to bottom, rgba(0,0,0,.2), rgba(0,0,0,.1)"
          alt="No Image"
          class="hnImage"
        >
          <form @submit.prevent="addChannel(PostInfo)">
            <div class="hnDiaryForm">
              <ul id="diarytitle">
                <v-text-field
                  label="diarytitle"
                  :rules="titleRules"
                  hide-details="auto"
                  counter="50"
                  v-model="PostInfo.title"
                  id="diarytitle"
                ></v-text-field>
              </ul>
              <ul id="diarydescription">
                <v-textarea
                  name="input-7-1"
                  counter="200"
                  :rules="desRules"
                  label="diarydescription"
                  v-model="PostInfo.description"
                  id="diarydescription"
                ></v-textarea>
              </ul>
              <ul id="diaryimage">
                <v-file-input
                  small-chips
                  accept="image/*"
                  label="diaryimage"
                  prepend-icon="mdi-camera"
                  @change="onFileChange"
                ></v-file-input>
              </ul>
              <button class="submit">만들기</button>
            </div>
          </form>
        </v-img>
        <v-icon class="back" @click="goHome">fas fa-arrow-left</v-icon>
      </v-card>
    </div>
  </v-container>
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
      },
      titleRules: [
        value => !!value || "제목을 입력해 주세요 :)",
        value => (value && value.length <= 50) || "제목은 최대 50자까지입니다."
      ],
      desRules: [
        value => !!value || "설명을 입력해 주세요 :)",
        value =>
          (value && value.length <= 200) || "설명은 최대 200자까지입니다."
      ]
    };
  },
  computed: {
    ...mapGetters(["getUserId"])
  },
  methods: {
    ...mapActions(["addChannel"]),
    onFileChange(file) {
      if (file) {
        this.PostInfo.file = file;
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
