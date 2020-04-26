import router from "../../router";

const HOST = process.env.VUE_APP_SERVER_HOST;
// const ALBUMBUCKETNAME = process.env.VUE_APP_BUCKET_NAME
// const BUCKETREGION = process.env.VUE_APP_BUCKET_REGION
// const IDENTIFYPOOL = process.env.VUE_APP_IDENTIFYPOOL

const axios = require("axios");
import AWS from "aws-sdk";

const state = {
  chanList: null,
  selectedChan: null,
  selectedDiary: null,
  commitDates: [new Date().getFullYear(), new Date().getMonth() + 1],
  commitInfo: [
    {
      "1일": 0,
      "2일": 1,
      "3일": 0,
      "4일": 1,
      "5일": 1,
      "6일": 1,
      "7일": 0,
      "8일": 1,
      "9일": 0,
      "10일": 1,
      "11일": 1,
      "12일": 0,
      "13일": 1,
      "14일": 1,
      "15일": 0,
      "16일": 1,
      "17일": 0,
      "18일": 1,
      "19일": 0,
      "20일": 1,
      "21일": 0,
      "22일": 1,
      "23일": 0,
      "24일": 1,
      "25일": 0,
      "26일": 1,
      "27일": 1,
      "28일": 0,
      "29일": 0,
      "30일": 1
    }
  ],
  nemos: [
    "nemo",
    "nemo",
    "nemo",
    "nemo",
    "nemo",
    "nemo",
    "nemo",
    "nemo",
    "nemo",
    "nemo",
    "nemo",
    "nemo",
    "nemo",
    "nemo",
    "nemo",
    "nemo",
    "nemo",
    "nemo",
    "nemo",
    "nemo",
    "nemo",
    "nemo",
    "nemo",
    "nemo",
    "nemo",
    "nemo",
    "nemo",
    "nemo",
    "nemo",
    "nemo",
    "nemo",
    "nemo",
    "nemo",
    "nemo",
    "nemo"
  ],
  s3: {},
  writerInfo: null
};

const getters = {
  getChanList: state => state.chanList,
  getSelectedChan: state => state.selectedChan,
  getSelectedDiary: state => state.selectedDiary,
  getCommitDates: state => state.commitDates,
  getCommitInfo: state => state.commitInfo,
  getNemos: state => state.nemos,
  getS3: state => state.s3,
  getWriterInfo: state => state.writerInfo
};

const mutations = {
  setChanList: (state, chanList) => (state.chanList = chanList),
  setSelectedChan: (state, channel) => (state.selectedChan = channel),
  setSelectedDiary: (state, diary) => (state.selectedDiary = diary),
  setNemos: (state, commitData) => {
    let results = [
      "nemo",
      "nemo",
      "nemo",
      "nemo",
      "nemo",
      "nemo",
      "nemo",
      "nemo",
      "nemo",
      "nemo",
      "nemo",
      "nemo",
      "nemo",
      "nemo",
      "nemo",
      "nemo",
      "nemo",
      "nemo",
      "nemo",
      "nemo",
      "nemo",
      "nemo",
      "nemo",
      "nemo",
      "nemo",
      "nemo",
      "nemo",
      "nemo",
      "nemo",
      "nemo",
      "nemo",
      "nemo",
      "nemo",
      "nemo",
      "nemo"
    ];
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
  sets3: (state, s3) => {
    state.s3 = s3;
  },
  setWriterInfo: (state, writerInfo) => (state.writerInfo = writerInfo)
};

const actions = {
  async bringChanList({ commit }) {
    const token = sessionStorage.getItem("jwt");
    const options = {
      headers: {
        Authorization: "JWT " + token
      }
    };
    await axios.get(HOST + "/channels/", options).then(message => {
      commit("setChanList", message.data.channels);
    });
  },
  addChannel: ({ commit }, PostInfo) => {
    commit;
    console.log(PostInfo);
    const token = sessionStorage.getItem("jwt");
    const options = {
      headers: {
        "Content-Type": "multipart/form-data",
        Authorization: "JWT " + token
      }
    };
    axios
      .post(
        HOST + "/channels/",
        {
          title: PostInfo.title,
          cover_image: PostInfo.image,
          description: PostInfo.description
        },
        options
      )
      .then(message => {
        console.log(message);
      });
  },
  bringChanDetail: ({ commit }, channelId) => {
    const token = sessionStorage.getItem("jwt");
    const options = {
      headers: {
        Authorization: "JWT " + token
      }
    };
    axios.get(`${HOST}/channels/${channelId}`, options).then(message => {
      commit("setSelectedChan", message.data);
      // console.log(message.data.title)
      router.push("postList");
    });
  },
  async deleteChan({ dispatch }, channelId) {
    const token = sessionStorage.getItem("jwt");
    const options = {
      headers: {
        Authorization: "JWT " + token
      }
    };
    await axios
      .delete(`${HOST}/channels/${channelId}`, options)
      .then(message => {
        message;
        alert("성공적으로 삭제되었습니다.");
      })
      .catch(message => {
        message;
        alert("삭제 중에 문제가 발생하였습니다.");
      });
    await dispatch("bringChanList");
    router.push("/");
  },
  bringDiaryDetail: ({ commit, getters }, diaryInfo) => {
    const token = sessionStorage.getItem("jwt");
    const options = {
      headers: {
        Authorization: "JWT " + token
      }
    };
    axios.get(`${HOST}/posts/${diaryInfo.pk}`, options).then(message => {
      commit("setSelectedDiary", message.data);
      const selectedChanUser = getters.getSelectedChan.user_set;
      for (let idx = 0; idx < selectedChanUser.length; idx++) {
        if (selectedChanUser[idx].id === message.data.user_id) {
          commit("setWriterInfo", selectedChanUser[idx]);
        }
      }
      router.push("/diaryDetail");
    });
  },
  //S3 부분
  s3Init: ({ commit }) => {
    AWS.config.update({
      region: process.env.VUE_APP_BUCKET_REGION,
      credentials: new AWS.CognitoIdentityCredentials({
        IdentityPoolId: process.env.VUE_APP_IDENTIFYPOOL
      })
    });
    const s3 = new AWS.S3({
      apiVersion: "2006-03-01",
      params: { Bucket: process.env.VUE_APP_BUCKET_NAME }
    });
    commit("sets3", s3);
  },
  async updates3({ commit }, PostInfo) {
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
  async addPost({ dispatch }, PostInfo) {
    // if (PostInfo.saveVideo) {
    //   await dispatch("s3Init");
    //   await dispatch("updates3", PostInfo);
    // }
    await dispatch("s3Init");
    await dispatch("updates3", PostInfo);
  }
};

export default {
  state,
  getters,
  mutations,
  actions
};
