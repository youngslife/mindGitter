const HOST = process.env.VUE_APP_SERVER_HOST;

const axios = require("axios");
import router from "../../router";
import AWS from "aws-sdk";
const state = {
  token: null,
  errors: [],
  loading: false,
  userName: null,
  userId: null,
  userInfoSet: null,
  userImgModal: false,
  commitDates: [new Date().getFullYear(), new Date().getMonth() + 1],
  commitInfo: null,
  userProfile: null,
  s3: {}
};

const getters = {
  isLoggedIn: state => !!state.token,
  getErrors: state => state.errors,
  isLoading: state => state.loading,
  getUserName: state => state.userName,
  getUserId: state => state.userId,
  getUserInfoSet: state => state.userInfoSet,
  getUserImgModal: state => state.userImgModal,
  getCommitDates: state => state.commitDates,
  getCommitInfo: state => state.commitInfo,
  getUserProfile: state => state.userProfile
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
  setUserImgModal: (state, userImgModal) => (state.userImgModal = userImgModal),
  setNemos: (state, commitData) => {
    let results = [];
    for (let i = 0; i < 105; i++) {
      results.push("nemo");
    }
    const pre = new Date(
      `${commitData.commitDates[0]}-${commitData.commitDates[1]}-01`
    ).getDay();
    const lastDay = new Date(
      commitData.commitDates[0],
      commitData.commitDates[1],
      0
    ).getDate();
    for (let cnt = 0; cnt < 35; cnt++) {
      if (cnt >= pre && cnt <= lastDay) {
        if (commitData.commitInfo[0][`${cnt}일`]) {
          results[cnt] = "red";
        } else {
          results[cnt] = "nemo";
        }
      }
    }
    state.nemos = results;
  },
  setUserProfile: (state, userProfile) => (state.userProfile = userProfile),
  sets3: (state, s3) => {
    state.s3 = s3;
  }
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
  login: ({ state, commit, getters, dispatch }, { username, password }) => {
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
          console.log(state.commitDates) // [2020, 04]
          console.log(token)
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
                  Accept: "application/json"
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
  bringUserInfoSet: ({ state, commit }) => {
    const token = sessionStorage.getItem("jwt");
    const options = {
      headers: {
        Authorization: "JWT " + token
      }
    };
    axios.get(`${HOST}/api/current_user`, options).then(message => {
      console.log(message.data);
      commit("setUserInfoSet", message.data);
      if (state.commitDates[1] > 3) {
        const startMonth = state.commitDates[1] - 3;
      }
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
  },
  s3Init: ({ commit }, type) => {
    AWS.config.update({
      region: process.env.VUE_APP_BUCKET_REGION,
      credentials: new AWS.CognitoIdentityCredentials({
        IdentityPoolId: process.env.VUE_APP_IDENTIFYPOOL
      })
    });
    const s3 = new AWS.S3({
      apiVersion: "2006-03-01",
      params: { Bucket: process.env.VUE_APP_BUCKET_NAME+'/'+type }
    });
    commit("sets3", s3);
  },
  async updates3({ commit }, PostInfo) {
    console.log('upadates3', PostInfo)
    const s3 = state.s3;
    const params = {
      Key: PostInfo.fileName,
      Body: PostInfo.file,
      ACL: "public-read-write"
    };
    const res = await s3.upload(params).promise();
    console.log(res);
    commit("sets3", {});
  },
  async bringUserProfile ({ commit }) {
    const token = sessionStorage.getItem("jwt");
    const options = {
      headers: {
        Authorization: "JWT " + token
      }
    };
    const res = await axios.get(`${HOST}/api/profile_img/`, options)
    console.log("bringUserProfile", res.data)
    commit("setUserProfile", res.data.profile_img)
  },
  async updateUserInfo ({ commit, dispatch }, PostInfo) {
    console.log('addChannel', PostInfo)
    await dispatch("s3Init", 'profile');
    await dispatch("updates3", PostInfo);
    const token = sessionStorage.getItem("jwt");
    const options = {
      headers: {
        Authorization: "JWT " + token
      }
    }
    const body = {
      profile_img: PostInfo.fileName
    }
    const res = await axios.put(`${HOST}/api/profile_img/`, body, options)
    console.log(res)
    await dispatch("bringUserProfile")
    commit("setUserImgModal", false)
  }
};

export default {
  state,
  getters,
  mutations,
  actions
};
