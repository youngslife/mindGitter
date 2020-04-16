<template>
  <div class="Login">
    <form>
      <h1>Signup</h1>
      <ul id="userId">
        ID
        <input type="text" id="userId" placeholder="아이디" />
      </ul>
      <ul id="userEmail">
        e-mail
        <input type="text" id="userEmail" placeholder="e-mail" />
      </ul>
      <ul id="userPassword">
        Password
        <input type="password" id="userPassword" placeholder="비밀번호" />
      </ul>
      <ul id="userPasswordConfirmation">
        Password
        <input
          type="password"
          id="userPasswordConfirmation"
          placeholder="비밀번호확인"
        />
      </ul>
      <a href="/login">Login</a>
    </form>
  </div>
</template>

<script>
export default {};
</script>

<style src="./Signup.css" scoped></style>
