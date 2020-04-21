const HOST = process.env.VUE_APP_SERVER_HOST;

const axios = require("axios");
import router from "../../router";

const state = {
  selectedChan: null
};

const getters = {
  getSelectedChan: state => state.selectedChan
};

const mutations = {
  setSelectedChan: (state, channel) => (state.selectedChan = channel)
};

const actions = {
  addDiary: ({ commit }, DiaryInfo) => {
    axios
      .post(HOST + "?", DiaryInfo, {
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json"
        }
      })
      .then(message => {
        message;
        router.push("/postList");
      })
      .catch(err => {
        if (!err.response) {
          commit("pushError", "Network Error..");
        } else {
          commit("pushError", "Some error occured");
        }
      });
  }
};

export default {
  state,
  getters,
  mutations,
  actions
};
