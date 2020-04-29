<template>
  <v-container class="hContainer">
    <v-carousel
      v-if="getChanList"
      :show-arrows="carOption"
      hide-delimiter-background
      delimiter-icon="mdi-minus"
      white
      height="98vh"
    >
      <template>
        <v-btn @click="goUserDetail" class="userPageBtn" fab small absolute>
          <v-icon>mdi-account-circle</v-icon>
        </v-btn>
      </template>
      <v-carousel-item v-for="(item, i) in getChanList" :key="i">
        <v-card
         dark
         style="border-radius:17px"
         @click="goDetail(item.id)"
        >
          <v-img 
            :src="imgAddr+item.cover_image"
            gradient="to bottom, rgba(0,0,0,.2), rgba(0,0,0,.1)"
            alt="No Image"
            class="cImage"
          >
            <div class="hContentBox">
              <p class="hTitle">{{ item.title }}</p>
              <p class="hSubTitle">
              {{ item.description }}</p>
              <div class="hMetaWrapper">
                <div class="hMetasBox">
                  <p class="hMeta">만든 날 </p>
                  <p class="hMeta">{{ getDate(item.created_at)}}</p>
                </div>
                <div class="hMetasBox">
                  <p class="hMeta">최근 작성일</p>
                  <p class="hMeta">{{ getDate(item.updated_at)}}</p>
                </div>
                <div class="hMetasBox">
                  <p class="hMeta">만든 이</p>
                  <p class="hMeta">{{ item.create_user.username }}</p>
                </div>
                <div class="hMetasBox">
                  <p class="hMeta">쓰는 이</p>
                  <p class="hMeta">{{ getPartyList(item.user_set) }}</p>
                </div>
              </div>
            </div>
            <div class="hNewBtn hBtnLeft" @click="goCreate">
              <v-icon color="rgba(255, 255, 255, 0.4)" small>mdi-text-box-plus-outline</v-icon>
            </div>
            <div class="hNewBtn hBtnRight">
              <v-icon color="rgba(255, 255, 255, 0.4)" small>mdi-account</v-icon>
            </div>
          </v-img>
        </v-card>
      </v-carousel-item>
    </v-carousel>
  </v-container>
</template>

<script>
import router from "@/router";
import { mapGetters, mapMutations, mapActions } from "vuex";

export default {
  name: "Home",
  data() {
    return {
      wHeight: 0,
      wWidth: 0,
      imgAddr: process.env.VUE_APP_STATIC_ADDR + "channel/",
      carOption: false,
      addImg:
        "https://w0.pngwave.com/png/106/279/computer-icons-medicine-health-care-plus-button-png-clip-art.png"
    };
  },
  methods: {
    ...mapActions(["bringChanList"]),
    ...mapMutations(["setChanId"]),
    goCreate() {
      router.push("createDiary");
    },
    //은영추가
    goUserDetail() {
      router.push("userDetail");
    },
    async goDetail(channelId) {
      // this.bringChanDetail(channelId);
      await this.setChanId(channelId);
      router.push("/postList")
    },
    getDate(stringd) {
      const d = new Date(stringd)
      return d.getFullYear() + "." + d.getMonth() + "." + d.getDate()
    },
    getPartyList(userset) {
      if (userset.length === 1) {
        return userset[0].username
      } else {
        return userset[0].username + '외 ' + userset.length + '명이'
      }
    }
  },
  computed: {
    ...mapGetters(["isLoggedIn", "getChanList"])
  },
  async created() {
    if (!this.isLoggedIn) {
      router.push("/login");
    } else {
      await this.bringChanList();
    }
  }
};
</script>

<style scoped src="./home.css"></style>
