<template>
  <div class="commitCalendar">
    <v-container @click="check">
      <v-row>
        <div class="first"></div>
        <div class="first">Mon</div>
        <div class="first"></div>
        <div class="first">Wed</div>
        <div class="first"></div>
        <div class="first">Fri</div>
        <div class="first"></div>
      </v-row>
      <v-row>
        <div :class="nemo" v-for="(nemo, i) in commitData.nemos.slice(0, 7)" :key="i"></div>
      </v-row>
      <v-row>
        <div :class="nemo" v-for="(nemo, i) in commitData.nemos.slice(7, 14)" :key="i"></div>
      </v-row>
      <v-row>
        <div :class="nemo" v-for="(nemo, i) in commitData.nemos.slice(14, 21)" :key="i"></div>
      </v-row>
      <v-row>
        <div :class="nemo" v-for="(nemo, i) in commitData.nemos.slice(21, 28)" :key="i"></div>
      </v-row>
      <v-row>
        <div :class="nemo" v-for="(nemo, i) in commitData.nemos.slice(28, 35)" :key="i"></div>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import { mapGetters, mapMutations } from "vuex";

export default {
  name: "commitCalendar",
  data() {
    return {
      commitData:{ 
        commitInfo: null,
        commitDates: null,
        nemos: null
      }
    };
  },
  computed: {
    ...mapGetters(["getCommitInfo", "getCommitDates", "getNemos"])
  },
  methods: {
    ...mapMutations(["setNemos"]),
    check() {
      this.setNemos(this.commitData);
      this.commitData.nemos = this.getNemos;
    }
  },
  created() {
    this.commitData.commitInfo = this.getCommitInfo;
    this.commitData.commitDates = this.getCommitDates;
    this.commitData.nemos = this.getNemos;
  }
};
</script>

<style src="./CommitCalendar.css" scoped></style>
