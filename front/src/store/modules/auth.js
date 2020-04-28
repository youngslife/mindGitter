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
  commitDates: [new Date().getFullYear(), new Date().getMonth()],
  commitInfo: null,
  indexDict: null,
  userProfile: null,
  s3: {},
  months: [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sept",
    "Oct",
    "Nov",
    "Dec"
  ],
  targetMonths: null
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
  getUserProfile: state => state.userProfile,
  getTargetMonths: state => state.targetMonths
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
  setUserProfile: (state, userProfile) => (state.userProfile = userProfile),
  sets3: (state, s3) => {
    state.s3 = s3;
  },
  setCommitInfo: (state, commitInfo) => (state.commitInfo = commitInfo),
  setIndexDict: (state, indexDict) => (state.indexDict = indexDict),
  setTargetMonths: (state, targetMonths) => (state.targetMonths = targetMonths)
};

const actions = {
  initialLogin: ({ commit }) => {
    const token = sessionStorage.getItem('jwt')
    if (token) {
        commit('setToken', token)
    }
},
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
          HOST + "/rest-auth/login/",
          { username, password },
          {
            headers: {
              "Content-Type": "application/json",
              Accept: "application/json"
            }
          }
        )
        .then(token => {
          console.log(state.commitDates); // [2020, 04]
          console.log(token);
          commit("setToken", token.data.token);
          commit("setLoading", false);
          commit("setUserName", username);
          commit("setUserId", token.data.user.pk);
          dispatch("preprocessingCommit");
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
              HOST + "/rest-auth/registration/",
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
  preprocessingCommit({ state, commit }) {
    commit;
    let targetMonths = [];
    const dates = new Date(state.commitDates[0], state.commitDates[1] + 1, 0);
    const nowEndYoil = dates.getDay();

    dates.setDate(dates.getDate() + 6 - nowEndYoil);

    const temp = new Date(state.commitDates[0], state.commitDates[1], 1);
    dates.setDate(dates.getDate() - 146);

    for (let i = 0; i < 5; i++) {
      targetMonths.push(
        `${temp.getFullYear()} - ${state.months[temp.getMonth()]}`
      );
      temp.setMonth(temp.getMonth() - 1);
    }
    commit("setTargetMonths", targetMonths);

    let indexDict = {};

    for (let i = 0; i < 147; i++) {
      if (dates.getMonth() < 9) {
        indexDict[
          `${dates.getFullYear()}-0${dates.getMonth() + 1}-${dates.getDate()}`
        ] = i;
      } else {
        indexDict[
          `${dates.getFullYear()}-${dates.getMonth() + 1}-${dates.getDate()}`
        ] = i;
      }
      dates.setDate(dates.getDate() + 1);
    }
    commit("setIndexDict", indexDict);
    let commitInfo = [];
    for (let i = 0; i < 147; i++) {
      commitInfo.push("nemo");
    }
    commit("setCommitInfo", commitInfo);

    console.log(targetMonths);
    console.log(indexDict);
  },
  async bringUserInfoSet({ commit }) {
    const token = sessionStorage.getItem("jwt");
    const options = {
      headers: {
        Authorization: "JWT " + token
      }
    };
    const message = await axios.get(`${HOST}/current_user`, options);
    commit("setUserInfoSet", message.data);
    let commitInfo = [];
    for (let i = 0; i < 147; i++) {
      commitInfo.push("nemo");
    }
    for (const post of message.data.post_set) {
      if (commitInfo[state.indexDict[post.created_at.slice(0, 10)]] == "nemo") {
        commitInfo[state.indexDict[post.created_at.slice(0, 10)]] = "done";
      }
    }
    commit("setCommitInfo", commitInfo);
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
      params: { Bucket: process.env.VUE_APP_BUCKET_NAME + "/" + type }
    });
    commit("sets3", s3);
  },
  async updates3({ commit }, PostInfo) {
    console.log("upadates3", PostInfo);
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
  async bringUserProfile({ commit }) {
    const token = sessionStorage.getItem("jwt");
    const options = {
      headers: {
        Authorization: "JWT " + token
      }
    };
    const res = await axios.get(`${HOST}/profile_img/`, options);
    console.log("bringUserProfile", res.data);
    commit("setUserProfile", res.data.profile_img);
  },
  async updateUserInfo({ commit, dispatch }, PostInfo) {
    console.log("addChannel", PostInfo);
    await dispatch("s3Init", "profile");
    await dispatch("updates3", PostInfo);
    const token = sessionStorage.getItem("jwt");
    const options = {
      headers: {
        Authorization: "JWT " + token
      }
    };
    const body = {
      profile_img: PostInfo.fileName
    };
    const res = await axios.put(`${HOST}/profile_img/`, body, options);
    console.log(res);
    await dispatch("bringUserProfile");
    commit("setUserImgModal", false);
  }
};

export default {
  state,
  getters,
  mutations,
  actions
};
