<template>
  <RegisterPage
    :login="isLogin"
    :developer="Boolean(true)"
    router-path="http://127.0.0.1:5000/developerlogin"
    router-push="/DeveloperDash"
    submit-text="Login"
    :options="this.options"
    route-text="Don't have a developer account?"
    route-path="/registerdev"
  >
  </RegisterPage>
</template>

<script>
import RegisterPage from '@/components/RegisterPage.vue';

const isLogin = Boolean(true);

export default {
  name: 'DevLoginView',
  components: {
    RegisterPage,
  },
  data() {
    return {
      isLogin,
      options: [
        { code: 'vu', name: 'Vue.js' },
        { code: 'ja', name: 'Java' },
        { code: 'py', name: 'Python' },
        { code: 'ru', name: 'Ruby' },
        { code: 'c++', name: 'C++' },
        { code: 'c', name: 'C' },
      ],
    };
  },
};
</script>

<style scoped>

.background {
  background: #3EB489;
  min-height: 100vh;
}

</style>
