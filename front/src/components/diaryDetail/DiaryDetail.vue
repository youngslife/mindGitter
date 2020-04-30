<template >
  <div class="ddContainer" v-if="getSelectedDiary && getWriterInfo">
    <div class="ddBar">
      <div class="ddBtn ddBackBtn" @click="goPostList">
        <v-icon color="rgba(0, 0, 0, 0.5)" small>fas fa-arrow-left</v-icon>
      </div>
      <p class="ddDate">{{ getDay(getSelectedDiary.created_at) }}</p>
      <div class="ddBtn ddHamBtn" @click="changeShowModal">
        <v-icon color="rgba(0, 0, 0, 0.5)" small>fas fa-ellipsis-v</v-icon>
      </div>
    </div>
    <div class="ddContentBox">
      <video
        controls
        width="100%"
        v-show="getSelectedDiary.is_save_video"
      > 
        <source :src="videoAddr + getSelectedDiary.video_file" />
      </video>
      <iframe 
        width="100%" 
        :src="defaultVideo" 
        frameborder="0"
        v-show="!getSelectedDiary.is_save_video"
        allow="accelerometer; encrypted-media; gyroscope; picture-in-picture" 
        allowfullscreen></iframe>
      <div class="ddTabBar">
        <div :class="mode==selectedMode ? 'ddSelectedTab':'ddTab'" v-for="mode in modes" :key="mode" @click="changeMode(mode)">
          <p :class="mode==selectedMode ? 'ddSelectedTabText':'ddTabText'">{{ mode }}</p>
        </div>
      </div>
      <div class="ddContent" v-if="(selectedMode =='Script') && ( getSelectedDiary.summary )">
        <div class="ddTitle" >
          <v-icon small>mdi-format-quote-open</v-icon>
          <p> {{ getSelectedDiary.title }} </p>
          <v-icon small>mdi-format-quote-close</v-icon>
        </div>
        <div class="ddAbb" >
          <p>{{ getSelectedDiary.summary }}</p>
        </div>
        <div class="ddTags">
          <span class="ddTag" v-for="(tag, idx) in getSelectedDiary.tags" :key="idx">
            #{{ tag }} 
          </span>
        </div>
        <div class="ddExpandBtn">
          <p v-show="!showFull" @click="showFull=!showFull">
            일기 펼치기
            <v-icon color="rgba(0, 0, 0, 0.4)">mdi-chevron-down</v-icon>
          </p>
          <p v-show="showFull" @click="showFull=!showFull">
            일기 접기
            <v-icon color="rgba(0, 0, 0, 0.5)">mdi-chevron-up</v-icon>
          </p>
        </div>
        <div v-show="showFull" class="ddContext">
          <p>{{ getSelectedDiary.context }}</p>
        </div>
      </div>
      <div class="ddYetContent" v-if="(selectedMode =='Script') && ( !getSelectedDiary.summary )">
        <img src="https://image.flaticon.com/icons/png/512/2422/2422071.png" alt="under construction">
        <p>아직 음성을 분석하는 중이에요 :)</p>
        <p>분석에 몇 분이 소요될 수 있습니다</p>
      </div>
      <div class="ddContent" v-if="selectedMode == 'Emotion' && ( getSelectedDiary.summary )">
        <div>
          <apexchart type="bubble" height="300" :options="getChartOptions" :series="getSeries"></apexchart>
        </div>
      </div>
      <div class="ddYetContent" v-if="(selectedMode =='Emotion') && ( !getSelectedDiary.summary )">
        <img src="https://image.flaticon.com/icons/png/512/2422/2422071.png" alt="under construction">
        <p>아직 감정을 분석하는 중이에요 :)</p>
        <p>분석에 몇 분이 소요될 수 있습니다</p>
      </div>
      <div class="ddContent" v-if="selectedMode == 'Comment'">
        <div v-if="getSelectedDiary.is_use_comment">
          <Comments />
        </div>
        <div v-else>
          <span>{{ selectedMode }}를 허용하지 않습니다.</span>
        </div>
      </div>
    </div>
    <div class="ddMeta">
      <p>
        {{ getSelectedDiary.created_at.slice(11, 13)+ "시 "+ 
        getSelectedDiary.created_at.slice(11, 16)+"분에 "+
        getWriterInfo.username + "가 촬영한 일기" }}
      </p>
    </div>
    <v-card v-if="showModal" @close="showModal = false">
      <div @click="editPost(getSelectedDiary)">
        <v-icon>fas fa-feather-alt</v-icon>수정
      </div>
      <div style="margin-bottom:3px" @click="deletePost(getSelectedDiary.pk)">
        <v-icon>fas fa-trash-alt</v-icon>삭제
      </div>
    </v-card>
  </div>
</template>
<script>
import router from "@/router";
import Comments from "./Comments/Comments.vue";
import { mapGetters, mapMutations, mapActions } from "vuex";
import VueApexcharts from "vue-apexcharts"


export default {
  name: "DiaryDetail",
  components: {
    Comments,
    apexchart: VueApexcharts
  },
  data() {
    return {
      modes: ["Script", "Emotion", "Comment"],
      selectedMode: "Script",
      videoAddr: process.env.VUE_APP_STATIC_ADDR + "diary/",
      writer: null,
      showModal: false,
      showFull: false,
      defaultVideo: 'https://www.youtube.com/embed/9Gd5C8XBzzw',
    }
  },
  computed: {
    ...mapGetters(["getChanName", "getSelectedDiary", "getWriterInfo", "getSeries", "getChartOptions"])
  },
  methods: {
    ...mapActions(["deleteDiary", "bringDiaryDetail", "bringEmotionData"]),
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
        this.deleteDiary(postId);
      }
    },
    async editPost(diaryInfo) {
      await this.setEditDiary(diaryInfo);
      router.push("/editPost");
    },
    getDay(d) {
      const raw = new Date(d)
      const month = raw.getMonth()+1
      return month+'월 '+raw.getDate() + '일'
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
    };
    console.log(this.getSelectedDiary)
    await this.bringEmotionData()
  }
};
</script>

<style src="./DiaryDetail.css" scoped></style>
