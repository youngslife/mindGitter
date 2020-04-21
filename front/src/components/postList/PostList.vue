<template>
  <div class="diaryList">
    <div class="infoAndSetting">
      <h1>{{ getSelectedChan }}</h1>
      <v-icon class="plus" @click="changeShowAddModal">fas fa-user-plus</v-icon>
      <v-card v-if="showAddModal" @close="showAddModal = false">
        <v-card-title>Share Diary</v-card-title>
        <v-card-text>
          친구 아이디
        </v-card-text>
        <input />
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn class="search" @click="changeShowAddModal">공유</v-btn>
          <v-btn class="close" @click="changeShowAddModal">닫기</v-btn>
        </v-card-actions>
      </v-card>
      <v-icon class="delete" @click="deleteChannel">fas fa-trash-alt</v-icon>
    </div>
    <div calss="search">
      <v-icon class="search" v-if="!showAddModal">fas fa-search</v-icon>
      <input type="text" v-model="searchTag" />
      <div class="sharedImage">
        <img
          class="sharedUserProfile"
          src="../../assets/shareduserprofile.jpg"
          alt="sharedUserProfile"
        />
      </div>
    </div>
    <div class="calendar">
      달력....
    </div>
    <div class="diaries">
      <div class="diaryInfo">
        <img
          src="../../assets/shareduserprofile.jpg"
          alt="userProfile"
          class="uImage"
        />
        <div class="content">
          <p class="title">첫 번째</p>
          <span class="tag">#첫 일기 #행복함 #재밌음</span>
        </div>
      </div>
      <div class="diaryInfo">
        <img
          src="../../assets/userprofile.jpg"
          alt="userProfile"
          class="uImage"
        />
        <div class="content">
          <p class="title">세 번째</p>
          <span class="tag">#공유신청 #기대됨 #얼른</span>
        </div>
      </div>
      <div class="diaryInfo">
        <img
          src="../../assets/userprofile.jpg"
          alt="userProfile"
          class="uImage"
        />
        <div class="content">
          <p class="title">두 번째</p>
          <span class="tag">#혼자심심 #공유할까? #지루함</span>
        </div>
      </div>
      <div class="diaryInfo">
        <img
          src="../../assets/userprofile.jpg"
          alt="userProfile"
          class="uImage"
        />
        <div class="content">
          <p class="title">일기장 만들었다</p>
          <span class="tag">#내가주인 #놀라움 #공유</span>
        </div>
      </div>
    </div>
    <Nav />
  </div>
</template>

<script>
import Nav from "../nav/Nav.vue";
import { mapGetters } from "vuex";

export default {
  name: "DiaryList",
  data() {
    return {
      searchTag: null,
      date: new Date(),
      showAddModal: false
    };
  },
  components: {
    Nav
  },
  computed: {
    ...mapGetters(["getSelectedChan"])
  },
  methods: {
    changeShowAddModal() {
      this.showAddModal = !this.showAddModal;
    },
    deleteChannel() {
      if (
        confirm(
          "일기장이 삭제되면 지금까지 작성하신 일기가 모두 삭제됩니다.\n삭제하시겠습니까?"
        )
      ) {
        console.log("삭제");
      } else {
        console.log("취소");
      }
    }
  }
};
</script>

<style src="./PostList.css" scoped></style>
