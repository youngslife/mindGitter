<template>
  <div class="Login">
    <form>
      <h1>Login</h1>
      <ul id="userId">
        ID
        <input type="text" id="userId" placeholder="아이디" />
      </ul>
      <ul id="userPassword">
        Password
        <input type="password" id="userPassword" placeholder="비밀번호" />
      </ul>
      <a href="/signup">Signup</a>
    </form>
  </div>
</template>

<script>
export default {};
</script>

<style src="./Login.css" scoped></style>
