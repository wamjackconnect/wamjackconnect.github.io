<template>
  <RegisterPage
    :developer="Boolean(true)"
    name-placeholder="Enter name"
    multi-placeholder="Select programming languages..."
    text-placeholder="Give a short description of your programming language expertise..."
    router-path="http://127.0.0.1:5000/registerdev"
    router-push="/CompanyDash"
    background-prop="#3EB489"
    submit-text="Sign Up"
    :options="options"
    route-text="Already have a developer account?"
    route-path="/developerlogin"
  >
  </RegisterPage>
</template>

<script>
import RegisterPage from '@/components/RegisterPage.vue';

export default {
  name: 'RegisterDevView',
  components: {
    RegisterPage,
  },
  data() {
    return {
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
