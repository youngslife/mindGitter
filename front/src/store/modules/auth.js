const HOST = process.env.VUE_APP_SERVER_HOST;

const axios = require("axios");
import router from "../../router";

const state = {
  token: null,
  errors: [],
  loading: false
};

const getters = {
  isLoggedIn: state => !!state.token,
  getErrors: state => state.errors,
  isLoading: state => state.loading
};

const mutations = {
  setLoading: (state, flag) => (state.loading = flag),
  setToken: (state, token) => {
    state.token = token;
    sessionStorage.setItem("jwt", token);
  },
  pushError: (state, error) => state.errors.push(error),
  clearErrors: state => (state.errors = [])
};

const actions = {
  logout: ({ commit }) => {
    commit("setToken", null);
    sessionStorage.removeItem("jwt");
    router.push("/login");
  },

  pushError: ({ commit }, error) => {
    commit("pushError", error);
  },

  login: ({ commit, getters }, { username, password }) => {
    if (getters.isLoggedIn) {
      router.push("/");
    } else {
      console.log(username, password);
      axios
        .post(
          HOST + "/api/rest_auth/login/",
          { username, password },
          {
            headers: {
              "Access-Control-Allow-Origin": "*",
              "Access-Control-Allow-Methods":
                "GET, POST, PATCH, PUT, DELETE, OPTIONS",
              "Access-Control-Allow-Headers":
                "Origin, Content-Type, X-Auth-Token"
            }
          }
        )
        .then(token => {
          commit("setToken", token.data.token);
          commit("setLoading", false);
          router.push("/");
        })
        .catch(err => {
          if (!err.response) {
            commit("pushError", "Network Error..");
          } else if (err.response.status === 400) {
            commit("pushError", "Invalid username or password");
          } else if (err.response.status === 500) {
            commit(
              "pushError",
              "Internal Server error. Please try again later"
            );
          } else {
            commit("pushError", "Some error occured");
          }
          commit("setLoading", false);
        });
    }
  },
  signup: (
    { commit, getters, dispatch },
    { username, email, password, passwordconfirmation }
  ) => {
    commit("clearErrors");
    if (getters.isLoggedIn) {
      router.push("/");
    } else {
      commit("clearErrors");
      if (!username) {
        commit("pushError", "ID를 입력하세요");
      }
      if (!email) {
        commit("pushError", "E-mail을 입력하세요");
      }
      if (password.length < 8) {
        commit("pushError", "비밀번호는 8자 이상어야 합니다");
      } else {
        if (password === passwordconfirmation) {
          console.log(username, email, password);
          axios
            .post(HOST + "/api/rest-auth/registration/", {
              username,
              email,
              password
            })
            .then(message => {
              message;
              const credentials = {
                username,
                password
              };
              dispatch("login", credentials);
            })
            .catch(err => {
              if (!err.response) {
                commit("pushError", "Network Error..");
              } else {
                commit("pushError", "Some error occured");
              }
            });
        } else {
          commit("pushError", "비밀번호가 일치하지 않습니다");
        }
      }
    }
  },
  initialLogin: ({ commit }) => {
    const token = sessionStorage.getItem("jwt");
    if (token) {
      commit("setToken", token);
    }
  },
  validation: ({ commit, dispatch }, credentials) => {
    commit("setLoading", false);
    commit("clearErrors");
    if (!credentials.username) {
      commit("pushError", "username can not be empty");
      commit("setLoading", false);
    }
    if (credentials.password < 8) {
      commit("pushError", "password too short");
      commit("setLoading", false);
    } else {
      dispatch("login", credentials);
    }
  }
};

export default {
  state,
  getters,
  mutations,
  actions
};
