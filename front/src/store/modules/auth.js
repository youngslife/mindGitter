const HOST = process.env.VUE_APP_SERVER_HOST;

const axios = require("axios");
import router from "../../router";

const state = {
  token: null,
  errors: [],
  loading: false,
  userName: null,
  userId: null,
  userInfoSet: null,
  userImgModal: false,
};

const getters = {
  isLoggedIn: state => !!state.token,
  getErrors: state => state.errors,
  isLoading: state => state.loading,
  getUserName: state => state.userName,
  getUserId: state => state.userId,
  getUserInfoSet: state => state.userInfoSet,
  getUserImgModal: state => state.userImgModal,
};

const mutations = {
  setLoading: (state, flag) => (state.loading = flag),
  setToken: (state, token) => {
    state.token = token;
    sessionStorage.setItem("jwt", token);
  },
  pushError: (state, error) => state.errors.push(error),
  clearErrors: state => (state.errors = []),
  setUserName: (state, userName) => (state.userName = userName),
  setUserId: (state, userId) => (state.userId = userId),
  setUserInfoSet: (state, userInfoSet) => (state.userInfoSet = userInfoSet),
  setUserImgModal: (state, userImgModal) => (state.userImgModal = userImgModal)
};

const actions = {
  logout: ({ commit }) => {
    commit("setToken", null);
    commit("setUserName", null);
    sessionStorage.removeItem("jwt");
    router.push("/login");
  },
  pushError: ({ commit }, error) => {
    commit("pushError", error);
  },
  login: ({ commit, getters, dispatch }, { username, password }) => {
    if (getters.isLoggedIn) {
      router.push("/");
    } else {
      axios
        .post(
          HOST + "/api/rest-auth/login/",
          { username, password },
          {
            headers: {
              "Content-Type": "application/json",
              Accept: "application/json"
            }
          }
        )
        .then(token => {
          commit("setToken", token.data.token);
          commit("setLoading", false);
          commit("setUserName", username);
          commit("setUserId", token.data.user.pk);
          dispatch("bringUserInfoSet");
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
    { username, email, password1, password2 }
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
      if (password1.length < 8) {
        commit("pushError", "비밀번호는 8자 이상어야 합니다");
      } else {
        if (password1 === password2) {
          axios
            .post(
              HOST + "/api/rest-auth/registration/",
              {
                username,
                email,
                password1,
                password2
              },
              {
                headers: {
                  "Content-Type": "application/json",
                  Accept: "application/json",
                }
              }
            )
            .then(message => {
              message;
              const credentials = {
                username,
                password: password1
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
  bringUserInfoSet: ({ commit }) => {
    commit;
    const token = sessionStorage.getItem("jwt");
    const options = {
      headers: {
        Authorization: "JWT " + token
      }
    };
    axios.get(`${HOST}/api/current_user`, options).then(message => {
      console.log(message.data);
    });
  },
  validation: ({ commit, dispatch }, { username, password }) => {
    commit("setLoading", false);
    commit("clearErrors");
    if (!username) {
      commit("pushError", "username can not be empty");
      commit("setLoading", false);
    }
    if (password < 8) {
      commit("pushError", "password too short");
      commit("setLoading", false);
    } else {
      dispatch("login", { username, password });
    }
  }
};

export default {
  state,
  getters,
  mutations,
  actions
};
