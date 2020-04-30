<template>
  <v-container class="hnContainer">
    <div class="hnDiary">
      <v-card
        dark
        style="border-radius:17px"
      >
        <v-img 
          :src="getCoverImage"
          gradient="to bottom, rgba(0,0,0,.2), rgba(0,0,0,.1)"
          alt="No Image"
          class="hnImage"
        >
          <form @submit.prevent="addChannel(PostInfo)">
            <div class="hnDiaryForm">
              <div>
                <v-text-field 
                  label="diarytitle" 
                  :rules="titleRules" 
                  hide-details="auto" 
                  counter="50"
                  v-model="PostInfo.title"
                  id="diarytitle"
                  
                ></v-text-field>
              </div>
              <div>
                <v-textarea
                  name="input-7-1"
                  counter="200"
                  :rules="desRules"
                  label="diarydescription"
                  v-model="PostInfo.description"
                  id="diarydescription"
                ></v-textarea>
              </div>
              <div>
                <p class="hnCoverTxt">cover image</p>
                <div class="hnCoverBox">
                  <div class="hnCoverWrapper" style="width:10vw; height:10vw" v-for="img in defaultImages" :key="img.index">
                    <img 
                      class="hnCoverSample"
                      @click="changeImage(img)"
                      :src="baseImageAddr+img" alt="" >
                  </div>
                </div>
              </div>
              <div style="margin-top:1vh">
                <v-file-input 
                  small-chips accept="image/*" 
                  label="diaryimage" 
                  clearable prepend-icon="mdi-file-image"
                  @change="onFileChange"
                ></v-file-input>
              </div>
              <div>
                <button class="submit">만들기</button>
              </div>
            </div>
          </form>
          <div class="hnBackBtn" @click="goHome">
            <v-icon color="rgba(255, 255, 255, 0.9)">fas fa-arrow-left</v-icon>
          </div>
          <div class="ddBtn ddHamBtn" @click="goUserDetail">
            <v-icon color="rgba(255, 255, 255, 0.9)" small>mdi-account</v-icon>
          </div>
        </v-img>
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
        fileName: this.getFileName ? this.getFileName : "default_channel1.jpg"
      },
      titleRules: [
        value => !!value || "제목을 입력해 주세요 :)",
        value => (value && value.length <= 50) || "제목은 최대 50자까지입니다."
      ],
      desRules: [
        value => !!value || '설명을 입력해 주세요 :)',
        value => (value && value.length <= 200) || '설명은 최대 200자까지입니다.'
      ],
      baseImageAddr: process.env.VUE_APP_STATIC_ADDR + "channel/default_channel",
      defaultImages: [
        '1.jpg', '2.jpg', '3.jpg', '4.jpg', '5.jpg', '6.jpg'
      ],
      coverImage: process.env.VUE_APP_STATIC_ADDR + "channel/default_channel1.jpg",
      file: null
    };
  },
  computed: {
    ...mapGetters(["getUserId"]),
    getCoverImage: function() {
      if (this.file) {
        const url = URL.createObjectURL(this.file)
        return url
      } else {
        return this.coverImage
      }
    },
    getFileName: function() {
      if (this.file) {
        return String(this.getUserId) + new Date().getTime() + ".jpg"
      } else {
        if (this.PostInfo.fileName) {
          return this.PostInfo.fileName
        } else {
          return "default_channel1.jpg"
        }
      }
    }
  },
  methods: {
    ...mapActions(["addChannel"]),
    changeImage(img) {
      this.file = null
      this.coverImage = this.baseImageAddr+img
      this.PostInfo.fileName = 'default_channel'+img
    },
    goHome() {
      router.push("/");
    },
    goUserDetail() {
      router.push("userDetail");
    },
    onFileChange(file) {
      console.log(file)
      if (file) {
        this.PostInfo.file = file;
        this.PostInfo.fileName =
          String(this.getUserId) + new Date().getTime() + ".jpg";
      } else {
        this.PostInfo.file = null;
        this.PostInfo.fileName = "default_channel1.jpg";
      }
    }
  }
};
</script>

<style src="./createDiary.css" scoped></style>
