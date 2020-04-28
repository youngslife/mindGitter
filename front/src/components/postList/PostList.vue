<template>
  <div class="diaryList" v-if="getSelectedChan && getDiaries">
    <div class="infoAndSetting">
      <h1>{{ getSelectedChan.title }}</h1>
      <v-icon class="settings" @click="changeShowModal">fas fa-cog</v-icon>
      <v-card v-if="showModal" @close="showModal = false" class="settings">
        <div class="addFri" @click="changeShowAddModal">
          <v-icon>fas fa-user-plus</v-icon>친구 초대
        </div>
        <div class="editChan" @click="editChan(getSelectedChan)">
          <v-icon>fas fa-feather-alt</v-icon>일기장 수정
        </div>
        <div class="withdraw" @click="withdraw(getSelectedChan.id)">
          <v-icon>fas fa-sign-out-alt</v-icon>일기장 탈퇴하기
        </div>
        <div class="delete" @click="deleteChannel(getSelectedChan.id)">
          <v-icon>fas fa-trash-alt</v-icon>일기장 삭제
        </div>
      </v-card>
      <v-card v-if="showAddModal" @close="showAddModal = false" class="invite">
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
    </div>
    <div calss="search">
      <v-icon class="search">fas fa-search</v-icon>
      <input type="text" v-model="searchTag" />
      <div
        class="sharedImage"
        v-for="(user, i) in getSelectedChan.user_set"
        :key="i"
      >
        <img
          class="sharedUserProfile"
          :src="showProfile(user.profile_img)"
          alt="sharedUserProfile"
        />
      </div>
    </div>
    <datepicker v-model="date" input-class="hi"></datepicker>
    <v-divider></v-divider>
    <div v-for="(diary, i) in getDiaries['dates']" :key="i">
      <div class="diaries" v-if="diary <= changeDate">
        <div class="date">
          {{ diary }}
        </div>
        <div
          class="diaryInfo"
          v-for="(item, idx) in getDiaries[diary]"
          :key="idx"
          @click="goDetail(item)"
        >
          <div
            class="userImage"
            v-for="(user, i) in getSelectedChan.user_set"
            :key="i"
          >
            <img
              v-if="user.id == item.user_id"
              :src="showProfile(user.profile_img)"
              alt="userProfile"
              class="uImage"
            />
          </div>
          <div class="content">
            <p class="title">{{ item.title }}</p>
            <div v-if="item.tags[0] != 'null'">
              <span class="tag" v-for="(tag, j) in item.tags" :key="j"
                >#{{ tag }}
              </span>
            </div>
            <div v-else>
              <span class="tag">
                <br />
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
    <Nav />
  </div>
</template>

<script>
import Nav from "../nav/Nav.vue";
import Datepicker from "vuejs-datepicker";
import { mapGetters, mapMutations, mapActions } from "vuex";
import router from "@/router";

export default {
  name: "DiaryList",
  data() {
    return {
      searchTag: null,
      date: new Date(),
      showAddModal: false,
      showModal: false,
      profileAddr: process.env.VUE_APP_STATIC_ADDR + "profile/"
    };
  },
  components: {
    Nav,
    Datepicker
  },
  computed: {
    ...mapGetters(["getSelectedChan", "getDiaries", "getChanId"]),
    changeDate() {
      if (this.date.getMonth() > 8) {
        if (this.date.getDate() > 9) {
          return `${this.date.getFullYear()}-${this.date.getMonth() +
            1}-${this.date.getDate()}`;
        } else {
          return `${this.date.getFullYear()}-${this.date.getMonth() +
            1}-0${this.date.getDate()}`;
        }
      } else {
        if (this.date.getDate() > 9) {
          return `${this.date.getFullYear()}-0${this.date.getMonth() +
            1}-${this.date.getDate()}`;
        } else {
          return `${this.date.getFullYear()}-0${this.date.getMonth() +
            1}-0${this.date.getDate()}`;
        }
      }
    }
  },
  methods: {
    ...mapActions([
      "deleteChan",
      "bringDiaryDetail",
      "bringChanDetail",
      "leaveChannel"
    ]),
    ...mapMutations(["setEditChan"]),
    changeShowAddModal() {
      this.showModal = false;
      this.showAddModal = !this.showAddModal;
    },
    changeShowModal() {
      this.showModal = !this.showModal;
    },
    deleteChannel(channelId) {
      this.showModal = !this.showModal;
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
    },
    showProfile(profile_img) {
      console.log(this.profileAddr + profile_img);
      return profile_img
        ? this.profileAddr + profile_img
        : require("../../assets/basic_userImage.png");
    },
    async withdraw(channelId) {
      this.showModal = !this.showModal;
      if (
        confirm(
          "일기장에서 탈퇴하시면 이 곳에서 작성한 일기는 다시 볼 수 없습니다.\n정말로 떠나시겠습니까?"
        )
      ) {
        console.log("탈퇴");
        await this.leaveChannel(channelId);
        // router.push("/");
      } else {
        console.log("취소");
      }
    },
    async editChan(channelInfo) {
      await this.setEditChan(channelInfo);
      router.push("/editChan");
    }
  },
  async created() {
    if (this.getChanId) {
      await this.bringChanDetail(this.getChanId);
    } else {
      router.push("/");
    }
  }
};
</script>

<style src="./PostList.css" scoped></style>
