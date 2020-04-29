<template>
  <v-container class="hContainer">
    <v-carousel
      v-if="getChanList"
      :show-arrows="carOption"
      hide-delimiter-background
      delimiter-icon="mdi-minus"
      light
      height="98vh"
    >
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
            <p
              style="font-size: 1.2em; color: rgba(255, 255, 255, 0.8);position:absolute; top:40%; left:50%; transform: translate(-50%, -50%)"
            >{{ item.title }}</p>
            <p style="font-size: 0.65em; color: rgba(255, 255, 255, 0.8); line-height:160%;position:absolute; top:49%; left:50%; width:70vw; transform: translate(-50%, -50%)">
            {{ item.description }}</p>

            <div
              style="
              background-color:rgba(255, 255, 255, 0.1); border-radius:5px; width:17.7vw; height: 5vh; 
              position:absolute; top:60%; left:20%; transform: translate(-50%, -50%);
              display:flex;justify-content:center;flex-direction:column;align-items:center"
            >
              <p class="hMeta">만든 날 </p>
              <p class="hMeta">{{ getDate(item.created_at)}}</p>
            </div>
            <div
              style="background-color:rgba(255, 255, 255, 0.1); border-radius:5px; width:17.7vw; height: 5vh; position:absolute; top:60%; left:40%; transform: translate(-50%, -50%);display:flex;justify-content:center;flex-direction:column;align-items:center"
            >
              <p class="hMeta">최근 작성일</p>
              <p class="hMeta">{{ getDate(item.updated_at)}}</p>
            </div>
            <div
              style="background-color:rgba(255, 255, 255, 0.1); border-radius:5px; width:17.7vw; height: 5vh; position:absolute; top:60%; left:60%; transform: translate(-50%, -50%);display:flex;justify-content:center;flex-direction:column;align-items:center"
            >
              <p class="hMeta">만든 이</p>
              <p class="hMeta">{{ item.create_user.username }}</p>
            </div>
            <div
              style="background-color:rgba(255, 255, 255, 0.1); border-radius:5px; width:17.7vw; height: 5vh; position:absolute; top:60%; left:80%; transform: translate(-50%, -50%);display:flex;justify-content:center;flex-direction:column;align-items:center"
            >
              <p class="hMeta">{{ getPartyList(item.user_set) }}</p>
              <p class="hMeta">{{ getParty(item.user_set) }}</p>
            </div>


          </v-img>
        </v-card>
      </v-carousel-item>
      <v-carousel-item>
        <h1>새 일기장</h1>
        <div class="aCon">
          <v-icon class="newBtn" @click="goCreate">mdi-plus</v-icon>
        </div>
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
<<<<<<< HEAD
    goDetail(channelId) {
      this.bringChanDetail(channelId);
    },
    getDate(stringd) {
      const d = new Date(stringd)
      return d.getFullYear() + "." + d.getMonth() + "." + d.getDate()
    },
    getParty(userset) {
      if (userset.length === 1) {
        return "혼자 쓰는 중"
      } else {
        return "함께 쓰는 중"
      }
    },
    getPartyList(userset) {
      if (userset.length === 1) {
        return userset[0].username
      } else {
        return userset[0].username + '외 ' + userset.length + '명이'
      }
=======
    async goDetail(channelId) {
      await this.setChanId(channelId);
      router.push("/postList");
>>>>>>> 28b30e40dd1d3b3d86cb19cbe44149965a3a0341
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
