<template>
  <div
    class="dairyDetail"
    v-if="getSelectedDiary && getChanName && getWriterInfo"
  >
    <v-icon class="back" @click="goPostList">fas fa-arrow-left</v-icon>
    <v-icon class="etc" @click="changeShowModal">fas fa-ellipsis-v</v-icon>
    <v-card v-if="showModal" @close="showModal = false">
      <div class="edit" @click="editPost(getSelectedDiary)">
        <v-icon>fas fa-feather-alt</v-icon>수정
      </div>
      <div class="delete" @click="deletePost(getSelectedDiary.pk)">
        <v-icon>fas fa-trash-alt</v-icon>삭제
      </div>
    </v-card>
    <h1>{{ getChanName }}</h1>
    <video
      width="100%"
      height="255px"
      controls
      class="dvideo"
      v-if="getSelectedDiary.is_save_video"
    >
      <source :src="videoAddr + getSelectedDiary.video_file" />
    </video>
    <div class="temp" v-if="getSelectedDiary.is_save_video"></div>
    <v-tabs fixed-tabs>
      <v-tab v-for="mode in modes" :key="mode" @click="changeMode(mode)">{{
        mode
      }}</v-tab>
    </v-tabs>
    <div class="text" v-if="selectedMode == 'Detail'">
      <h3>{{ getSelectedDiary.title }}</h3>
      <div class="tags" v-if="getSelectedDiary.tags[0] != 'null'">
        <span v-for="(tag, idx) in getSelectedDiary.tags" :key="idx"
          >#{{ tag }}
        </span>
      </div>
      <div class="context" v-if="getSelectedDiary.summary">
        {{ getSelectedDiary.summary }}
      </div>
      <div class="context" v-else>
        아직 영상에 대한 분석이 끝나지 않았습니다.<br /><br />
        조금만 기다려주세요 :D
      </div>
    </div>
    <div class="text" v-if="selectedMode == 'Analysis'">
      <div class="analysis" v-if="getSelectedDiary.emotion">
        <span>{{ getSelectedDiary.emotion }}</span>
      </div>
      <div class="analysis" v-else>
        아직 영상에 대한 분석이 끝나지 않았습니다.<br /><br />
        조금만 기다려주세요 :D
      </div>
    </div>
    <div class="text" v-if="selectedMode == 'Comment'">
      <!-- <span>{{ selectedMode }}</span> -->
      <div v-if="getSelectedDiary.is_use_comment">
        <Comments />
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
          `${getSelectedDiary.created_at.slice(
            0,
            10
          )}  ${getSelectedDiary.created_at.slice(11, 16)}`
        }}</span
      >
    </div>
  </div>
</template>

<script>
import router from "@/router";
import Comments from "./Comments/Comments.vue";
import { mapGetters, mapMutations, mapActions } from "vuex";

export default {
  name: "DiaryDetail",
  components: {
    Comments
  },
  data() {
    return {
      modes: ["Detail", "Analysis", "Comment"],
      selectedMode: "Detail",
      videoAddr: process.env.VUE_APP_STATIC_ADDR + "diary/",
      writer: null,
      showModal: false
    };
  },
  computed: {
    ...mapGetters(["getChanName", "getSelectedDiary", "getWriterInfo"])
  },
  methods: {
    ...mapActions(["deleteDiary", "bringDiaryDetail"]),
    ...mapMutations(["setEditDiary", "setPostId", "setChanName"]),
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
  async created() {
    const postId = sessionStorage.getItem("post");
    const chanName = sessionStorage.getItem("chanName");
    if (postId) {
      await this.setChanName(chanName);
      await this.bringDiaryDetail(postId);
      await this.setPostId(postId);
    } else {
      router.push("/");
    }
  }
};
</script>

<style src="./DiaryDetail.css" scoped></style>
