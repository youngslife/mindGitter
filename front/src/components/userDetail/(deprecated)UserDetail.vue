<template>
  <v-container class="userDetail">
    <v-row class="userId">
      <p v-if="isLoggedIn">
        {{ getUserName }}
      </p>
      <button class="settings" @click.prevent="logout">
        <v-icon>fas fa-sign-out-alt</v-icon>
      </button>
    </v-row>
    <v-row class="profile">
      <v-col cols="3">
        <img
          class="userprofile"
          src="../../assets/userprofile.jpg"
          alt="userprofile"
        />
      </v-col>
      <v-col cols="9" class="infoTotal">
        <v-row>
          <v-col class="infoName">
            <v-row>
              First
            </v-row>
            <v-row>
              First Date
            </v-row>
          </v-col>
          <v-col class="infoName">
            <v-row>
              Total
            </v-row>
            <v-row>
              total posts
            </v-row>
          </v-col>
          <v-col class="infoName">
            <v-row>
              Channel
            </v-row>
            <v-row>
              number of channel
            </v-row>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
    <div class="commitCalendar">
      <CalendarHeatmap
        endDate="2020-12-31"
        :values="[
          { date: '2020-04-20', count: 5 },
          { date: '2020-04-19', count: 3 },
          { date: '2020-04-17', count: 4 },
          { date: '2020-04-15', count: 2 },
          { date: '2020-04-12', count: 1 },
          { date: '2020-04-10', count: 4 },
          { date: '2020-04-6', count: 6 },
        ]"
      />
    </div>
    <div class="emotion">
      <h3>Emotion</h3>
      <div class="emotionDetail">
        감정 분석 결과
      </div>
    </div>
    <div class="tag">
      <h3>Tag</h3>
      <div class="tagDetail">
        tag 분석 결과
      </div>
    </div>
    <Nav />
  </v-container>
</template>

<script>
import Nav from "../nav/Nav.vue";
import { CalendarHeatmap } from "vue-calendar-heatmap";
import { mapGetters, mapActions } from "vuex";

export default {
  name: "UserDetail",
  components: {
    Nav,
    CalendarHeatmap,
  },
  computed: {
    ...mapGetters(["getUserName", "isLoggedIn"]),
  },
  methods: {
    ...mapActions(["logout"]),
  },
};
</script>

<style src="./UserDetail.css" scoped></style>
