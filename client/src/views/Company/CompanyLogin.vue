<template>
  <RegisterPage
    :login="isLogin"
    :developer="Boolean(false)"
    router-path="http://127.0.0.1:5000/companylogin"
    router-push="/CompanyDash"
    submit-text="Login"
    :options="options"
    route-text="Don't have a company account?"
    route-path="/registercom"
  >
  </RegisterPage>
</template>

<script>
import RegisterPage from '@/components/RegisterPage.vue';

const isLogin = Boolean(true);

export default {
  name: 'CompLoginView',
  components: {
    RegisterPage,
  },
  data() {
    return {
      isLogin,
      options: [
        { name: 'Games' },
        { name: 'News' },
        { name: 'Software' },
        { name: 'Social Media' },
        { name: 'Security' },
        { name: 'Logistics' },
      ],
    };
  },
};
</script>

<style scoped>

.background {
  background: #f1efd7;
  min-height: 100vh;
}

</style>
