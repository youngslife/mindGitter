<template>
  <div class="userName">
    {{ this.username }}
  </div>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      username: null,
    };
  },
  props: {
    userpk: Number,
  },
  async mounted() {
    const token = sessionStorage.getItem("jwt");
    const HOST = process.env.VUE_APP_SERVER_HOST;
    const options = {
      headers: {
        Authorization: "JWT " + token,
      },
    };
    await axios.get(`${HOST}/user/${this.userpk}`, options).then(res => {
        this.username = res.data.username
    })
  },
};
</script>

<style src="./UserName.css" scoped></style>
