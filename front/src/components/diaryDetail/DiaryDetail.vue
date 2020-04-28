<template>
  <div class="dairyDetail">
    <v-icon class="back" @click="goPostList">fas fa-arrow-left</v-icon>
    <v-icon class="etc" @click="changeShowModal">fas fa-ellipsis-v</v-icon>
    <v-card v-if="showModal" @close="showModal = false">
      <div class="edit" @click="editPost(selectedDiary)">
        <v-icon>fas fa-pen</v-icon>수정
      </div>
      <div class="delete" @click="deletePost(selectedDiary.pk)">
        <v-icon>fas fa-trash-alt</v-icon>삭제
      </div>
    </v-card>
    <h1>{{ getSelectedChan.title }}</h1>
    <video
      width="100%"
      height="255px"
      controls
      class="dvideo"
      v-if="selectedDiary.is_save_video"
    >
      <source :src="videoAddr + selectedDiary.video_file" />
    </video>
    <div class="temp" v-if="selectedDiary.is_save_video"></div>
    <v-tabs fixed-tabs>
      <v-tab v-for="mode in modes" :key="mode" @click="changeMode(mode)">{{
        mode
      }}</v-tab>
    </v-tabs>
    <div class="text" v-if="selectedMode == 'Detail'">
      <h3>{{ selectedDiary.title }}</h3>
      <div class="tags" v-if="selectedDiary.tags[0] != 'null'">
        <span v-for="(tag, idx) in selectedDiary.tags" :key="idx"
          >#{{ tag }}
        </span>
      </div>
      <div class="context">
        {{ selectedDiary.context }}
      </div>
    </div>
    <div class="text" v-if="selectedMode == 'Analysis'">
      <span>{{ selectedMode }}</span>
    </div>
    <div class="text" v-if="selectedMode == 'Comment'">
      <div v-if="selectedDiary.is_use_comment">
        <span>{{ selectedMode }}</span>
      </div>
      <div v-else>
        <span>{{ selectedMode }}를 허용하지 않습니다.</span>
      </div>
    </div>
    <div class="additionalInfo">
      <span>작성자: {{ getWriterInfo.username }}</span>
      <br />
      <span
        >작성시간:
        {{
          `${selectedDiary.created_at.slice(
            0,
            10
          )}  ${selectedDiary.created_at.slice(11, 16)}`
        }}</span
      >
    </div>
  </div>
</template>

<script>
import router from "@/router";
import { mapGetters, mapMutations, mapActions } from "vuex";

export default {
  name: "DiaryDetail",
  data() {
    return {
      modes: ["Detail", "Analysis", "Comment"],
      selectedMode: "Detail",
      selectedDiary: "",
      videoAddr: process.env.VUE_APP_STATIC_ADDR + "diary/",
      writer: null,
      showModal: false
    };
  },
  computed: {
    ...mapGetters(["getSelectedChan", "getSelectedDiary", "getWriterInfo"])
  },
  methods: {
    ...mapActions(["deleteDiary"]),
    ...mapMutations(["setEditDiary"]),
    goPostList() {
      router.push("/postList");
    },
    changeMode(mode) {
      this.selectedMode = mode;
    },
    changeShowModal() {
      this.showModal = !this.showModal;
    },
    deletePost(postId) {
      this.showModal = !this.showModal;
      if (
        confirm("삭제된 내용은 복구가 불가능합니다\n정말 삭제하시겠습니까?")
      ) {
        console.log("삭제");
        this.deleteDiary(postId);
      } else {
        console.log("취소");
      }
    },
    async editPost(diaryInfo) {
      await this.setEditDiary(diaryInfo);
      router.push("/editPost");
    }
  },
  created() {
    this.selectedDiary = this.getSelectedDiary;
    console.log(this.selectedDiary.video_file);
  }
};
</script>

<style src="./DiaryDetail.css" scoped></style>
