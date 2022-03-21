<template>
  <RegisterPage
    :developer="Boolean(false)"
    name-placeholder="Enter company name"
    multi-placeholder="Select general industries..."
    text-placeholder="Give a short description of your company and its goals..."
    router-path="http://127.0.0.1:5000/registercom"
    router-push="/CompanyDash"
    submit-text="Sign Up"
    :options="options"
    route-text="Already have a company account?"
    route-path="/companylogin"
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
  background-size: cover;
}

</style>
