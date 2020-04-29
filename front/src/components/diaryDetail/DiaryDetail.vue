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
        v-if="getSelectedDiary.is_save_video"
      > 
        <source :src="videoAddr + getSelectedDiary.video_file" />
      </video>
      <div class="ddTabBar">
        <div :class="mode==selectedMode ? 'ddSelectedTab':'ddTab'" v-for="mode in modes" :key="mode" @click="changeMode(mode)">
          <p :class="mode==selectedMode ? 'ddSelectedTabText':'ddTabText'">{{ mode }}</p>
        </div>
      </div>
      <div class="ddContent" v-if="selectedMode == 'Script'">
        <div class="ddTitle" >
          <v-icon small>mdi-format-quote-open</v-icon>
          <p> {{ getSelectedDiary.title }} </p>
          <v-icon small>mdi-format-quote-close</v-icon>
        </div>
        <div class="ddAbb" >
          <p>{{ fakeAbb }}</p>
        </div>
        <div class="ddTags">
          <span class="ddTag" v-for="(tag, idx) in fakeTags" :key="idx">
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
          <p>{{ fakeContent }}</p>
        </div>
      </div>

      <div class="ddContent" v-if="selectedMode == 'Emotion'">
        <span>{{ selectedMode }}</span>
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
<!-- <div class="tags" v-if="getSelectedDiary.tags[0] != 'null'">
  <span v-for="(tag, idx) in getSelectedDiary.tags" :key="idx">
    #{{ tag }}
  </span>
</div> -->
        <!-- <div class="context">
  <p>{{ getSelectedDiary.context }}</p>
</div> -->
<!-- <div class="context">
  <p>{{ getSelectedDiary.context }}</p>
</div> -->
<script>
import router from "@/router";
// import Comments from "./Comments/Comments.vue";
import { mapGetters, mapMutations, mapActions } from "vuex";

export default {
  name: "DiaryDetail",
  components: {
    // Comments
  },
  data() {
    return {
      modes: ["Script", "Emotion", "Comment"],
      selectedMode: "Script",
      videoAddr: process.env.VUE_APP_STATIC_ADDR + "diary/",
      writer: null,
      showModal: false,
      showFull: false,
      fakeContent: "오늘은 좀 작가 속이 많이 상한 날인데요. 진짜 많이 사용한다. 일단 진짜 오랫동안 친하게 지냈던 거의 십 년 가까이 그랬던 친구랑 약간 심하게 다퉈했는데 한 번도 있었던 일이 아니었어. 적응도 안되고 답답하고 무슨 말을 먼저 끝내야 될지 모르겠다는 생각이 조금 들어서 약간 그런 속상한 마음에 카메라를 잠시 키우게 됐습니다. 사실 이런 거 싸우는 것은 정말 사소한 과 하나로 싸우게 되거든요. 간 사소한 일, 사선, 감정 이런 걸로 싸우게 되는데 시간이 알아서 해결해 주겠다. 시간을 견디는 저 스스로가 좀 힘들 수 있겠지만 같은 어떻게 보면 진짜 별일 아닌 건데 빨리 해결됐으면 좋겠네요. 그리고는 직접 표가 아니라고 생각한다. 아무튼 속은 조금 풀린것 같으니 빠른 시일 내에 친구나 화해를 해야겠네요.",
      fakeTags: ["친구", "시간", "일", "해결", "생각", "속"],
      fakeAbb: "적응도 안되고 답답하고 무슨 말을 먼저 끝내야 될지 모르겠다는 생각이 조금 들어서 약간 그런 속상한 마음에 카메라를 잠시 키우게 됐습니다."
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
  }
};
</script>

<style src="./DiaryDetail.css" scoped></style>
