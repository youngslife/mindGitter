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
        <v-card-text style="font-weight:bold; margin-top:20px">
          친구 아이디 검색하기
        </v-card-text>
        <div style="width:80%; margin: 0 auto;">
          <v-text-field
            label="name"
            v-model="noticeInfo.username"
            @keydown.enter="pushNotice(getSelectedChan.id)"
            append-icon="mdi-account-search"
          ></v-text-field>
        </div>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn class="search" @click="pushNotice(getSelectedChan.id)"
            >요청</v-btn
          >
          <v-btn class="close" @click="changeShowAddModal">닫기</v-btn>
          <v-spacer></v-spacer>
        </v-card-actions>
      </v-card>
    </div>
    <div calss="search">
      <v-icon class="search">fas fa-search</v-icon>
      <input
        type="text"
        v-model="searchParams.searchKwd"
        @keydown.enter="searchingTag(searchParams)"
        placeholder="search tag"
      />
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
        <div class="date">{{ diary }}</div>
        <div
          class="diaryInfo"
          v-for="(item, idx) in getDiaries[diary]"
          :key="idx"
          @click="goDetail(item.pk)"
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
            <div v-if="item.tags.length">
              <span class="tag" v-for="(tag, j) in item.tags" :key="j"
                >#{{ tag }}
              </span>
            </div>
            <div v-else>
              <span class="tag">
                분석중입니다.
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
      //은영
      noticeInfo: {
        username: "",
        channel_id: ""
      },
      // searchTag: null,
      searchParams: {
        searchKwd: null,
        channId: null
      },
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
    ...mapMutations(["setPostId", "setEditChan"]),
    ...mapActions([
      "deleteChan",
      "bringDiaryDetail",
      "bringChanDetail",
      "leaveChannel",
      "addNotification",
      "searchingTag"
    ]),
    pushNotice(channelId) {
      this.noticeInfo.channel_id = channelId;
      if (
        confirm(`${this.noticeInfo.username}님께 공유 요청을 보내시겠습니까?`)
      ) {
        this.addNotification(this.noticeInfo);
        alert("공유 요청을 보냈습니다 :) 상대방이 수락하면 쓰는 이에 추가됩니다")
      }
      this.showAddModal = false;
    },
    //
    changeShowAddModal() {
      this.noticeInfo.username = null;
      this.noticeInfo.channel_id = null;
      this.showModal = false;
      this.showAddModal = !this.showAddModal;
    },
    changeShowModal() {
      if (this.showAddModal) {
        this.showAddModal = false;
      }
      this.showModal = !this.showModal;
    },
    deleteChannel(channelId) {
      this.showModal = !this.showModal;
      if (
        confirm(
          "일기장이 삭제되면 지금까지 작성하신 일기가 모두 삭제됩니다.\n삭제하시겠습니까?"
        )
      ) {
        this.deleteChan(channelId);
      }
    },
    async goDetail(diaryPK) {
      await this.setPostId(diaryPK);
      await this.bringDiaryDetail(diaryPK);
      router.push("/diaryDetail");
    },
    showProfile(profile_img) {
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
        await this.leaveChannel(channelId);
      }
    },
    async editChan(channelInfo) {
      await this.setEditChan(channelInfo);
      router.push("/editChan");
    }
  },
  async created() {
    const chanpk = sessionStorage.getItem("chan");
    if (chanpk) {
      await this.bringChanDetail(chanpk);
    } else {
      router.push("/");
    }
  }
};
</script>

<style src="./PostList.css" scoped></style>
