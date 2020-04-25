<template>
  <div class="diaryList">
    <div class="infoAndSetting">
      <h1>{{ selectedChan.title }}</h1>
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
      <v-icon class="delete" @click="deleteChannel(selectedChan.id)"
        >fas fa-trash-alt</v-icon
      >
    </div>
    <div calss="search">
      <v-icon class="search">fas fa-search</v-icon>
      <input type="text" v-model="searchTag" />
      <div class="sharedImage">
        <img
          class="sharedUserProfile"
          src="../../assets/shareduserprofile.jpg"
          alt="sharedUserProfile"
        />
        <img
          class="sharedUserProfile"
          src="../../assets/userprofile.jpg"
          alt="sharedUserProfile"
        />
      </div>
    </div>
    <datepicker v-model="date" input-class="hi"></datepicker>
    <v-divider></v-divider>
    <div class="diaries">
      <div
        class="diaryInfo"
        v-for="(item, idx) in getSelectedChan.post_set"
        :key="idx"
        @click="goDetail(item)"
      >
        <!-- <div class="diaryInfo" @click="goDetail(diaries[0])"> -->
        <img
          src="../../assets/userprofile.jpg"
          alt="userProfile"
          class="uImage"
        />
        <div class="content">
          <p class="title">{{ item.title }}</p>
          <span class="tag" v-for="(tag, i) in item.tags" :key="i"
            >#{{ tag }}
          </span>
        </div>
      </div>
    </div>
    <Nav />
  </div>
</template>

<script>
import Nav from "../nav/Nav.vue";
import Datepicker from "vuejs-datepicker";
import { mapGetters, mapActions } from "vuex";

export default {
  name: "DiaryList",
  data() {
    return {
      searchTag: null,
      date: new Date(),
      showAddModal: false,
      selectedChan: null
    };
  },
  components: {
    Nav,
    Datepicker
  },
  computed: {
    ...mapGetters(["getSelectedChan"])
  },
  methods: {
    ...mapActions(["deleteChan", "bringDiaryDetail"]),
    changeShowAddModal() {
      this.showAddModal = !this.showAddModal;
    },
    deleteChannel(channelId) {
      if (
        confirm(
          "일기장이 삭제되면 지금까지 작성하신 일기가 모두 삭제됩니다.\n삭제하시겠습니까?"
        )
      ) {
        console.log("삭제");
        this.deleteChan(channelId);
      } else {
        console.log("취소");
      }
    },
    goDetail(diaryInfo) {
      this.bringDiaryDetail(diaryInfo);
    }
  },
  beforeMount() {
    this.selectedChan = this.getSelectedChan;
  }
};
</script>

<style src="./PostList.css" scoped></style>
