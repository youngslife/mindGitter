const HOST = process.env.VUE_APP_SERVER_HOST;

const axios = require("axios");
import router from "../../router";

const state = {
  selectedChan: null,
  selectedDiary: null,
  commitDates: [new Date().getFullYear(), new Date().getMonth() + 1],
  commitInfo: [{"1일": 0, "2일": 1, "3일": 0, "4일": 1, "5일": 1, "6일":1, "7일": 0, "8일": 1, "9일": 0, "10일": 1, "11일": 1, "12일": 0, "13일": 1, "14일": 1, "15일": 0, "16일": 1, "17일": 0, "18일": 1, "19일": 0, "20일": 1, "21일": 0, "22일": 1, "23일": 0, "24일": 1, "25일": 0, "26일": 1, "27일": 1, "28일": 0, "29일":0, "30일": 1}],
  nemos: ["nemo", "nemo", "nemo", "nemo", "nemo", "nemo", "nemo", "nemo", "nemo", "nemo", "nemo", "nemo", "nemo", "nemo", "nemo", "nemo", "nemo", "nemo", "nemo", "nemo", "nemo", "nemo", "nemo", "nemo", "nemo", "nemo", "nemo", "nemo", "nemo", "nemo", "nemo", "nemo", "nemo", "nemo", "nemo"]
};

const getters = {
  getSelectedChan: state => state.selectedChan,
  getSelectedDiary: state => state.selectedDiary,
  getCommitDates: state => state.commitDates,
  getCommitInfo: state => state.commitInfo,
  getNemos: state => state.nemos
};

const mutations = {
  setSelectedChan: (state, channel) => (state.selectedChan = channel),
  setSelectedDiary: (state, diary) => (state.selectedDiary = diary),
  setNemos: (state, commitData) => {
    let results = ["nemo", "nemo", "nemo", "nemo", "nemo", "nemo", "nemo", "nemo", "nemo", "nemo", "nemo", "nemo", "nemo", "nemo", "nemo", "nemo", "nemo", "nemo", "nemo", "nemo", "nemo", "nemo", "nemo", "nemo", "nemo", "nemo", "nemo", "nemo", "nemo", "nemo", "nemo", "nemo", "nemo", "nemo", "nemo"];
    const pre = new Date(`${commitData.commitDates[0]}-${commitData.commitDates[1]}-01`).getDay();
    const lastDay = new Date(commitData.commitDates[0], commitData.commitDates[1], 0).getDate();
    for (let cnt = 0; cnt < 35; cnt++) {
      if (cnt >= pre && cnt <= lastDay) {
        if (commitData.commitInfo[0][`${cnt}일`]) {
          results[cnt] = "red";
        } else {
          results[cnt] = "nemo"
        }
      }
    }
    state.nemos = results;
  }
};

const actions = {
  addDiary: ({ commit }, DiaryInfo) => {
    axios
      .post(HOST + "?", DiaryInfo, {
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
      })
      .then((message) => {
        message;
        router.push("/postList");
      })
      .catch((err) => {
        if (!err.response) {
          commit("pushError", "Network Error..");
        } else {
          commit("pushError", "Some error occured");
        }
      });
  },
  addPost: ({ commit }, PostInfo) => {
    console.log(PostInfo)
    commit("pushError", "Success")
  },
};

export default {
  state,
  getters,
  mutations,
  actions,
};
