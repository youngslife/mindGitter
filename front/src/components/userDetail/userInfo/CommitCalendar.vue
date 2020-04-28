<template>
  <div class="commitCalendar">
    <v-container v-if="getCommitInfo">
      <!-- 월 -->
      <v-row class="month">
        <v-col class="first"></v-col>
        <v-col></v-col>
        <v-col></v-col>
        <v-col>
          <div class="first">{{ getTargetMonths[4].slice(7) }}</div>
        </v-col>
        <v-col></v-col>
        <v-col></v-col>
        <v-col></v-col>
        <v-col>
          <div class="first">{{ getTargetMonths[3].slice(7) }}</div>
        </v-col>
        <v-col></v-col>
        <v-col></v-col>
        <v-col></v-col>
        <v-col>
          <div class="first">{{ getTargetMonths[2].slice(7) }}</div>
        </v-col>
        <v-col></v-col>
        <v-col></v-col>
        <v-col></v-col>
        <v-col>
          <div class="first">{{ getTargetMonths[1].slice(7) }}</div>
        </v-col>
        <v-col></v-col>
        <v-col></v-col>
        <v-col></v-col>
        <v-col>
          <div class="first">{{ getTargetMonths[0].slice(7) }}</div>
        </v-col>
        <v-col></v-col>
        <v-col></v-col>
        <v-col></v-col>
      </v-row>
      <v-row>
        <v-col class="first">
          <div class="first"></div>
          <div class="first">Mon</div>
          <div class="first"></div>
          <div class="first">Wed</div>
          <div class="first"></div>
          <div class="first">Fri</div>
          <div class="first"></div>
        </v-col>
        <v-col v-for="(cnt, i) in count" :key="i">
          <div
            :class="nemo"
            v-for="(nemo, i) in getCommitInfo.slice(cnt * 7 + 0, cnt * 7 + 7)"
            :key="i"
          ></div>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex";

export default {
  name: "commitCalendar",
  data() {
    return {
      count: [
        0,
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        12,
        13,
        14,
        15,
        16,
        17,
        18,
        19,
        20
      ],
      commitData: {
        commitInfo: null,
        commitDates: null,
        nemos: null
      }
    };
  },
  computed: {
    ...mapGetters(["getCommitInfo", "getTargetMonths"])
  },
  methods: {
    ...mapActions(["bringUserInfoSet"])
  },
  async created() {
    this.bringUserInfoSet();
  }
};
</script>

<style src="./CommitCalendar.css" scoped></style>
