import Vue from "vue";
import Vuex from "vuex";
import auth from "./modules/auth";
import diary from "./modules/diary";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    userName: null
  },
  mutations: {},
  actions: {},
  modules: {
    auth,
    diary
  }
});
