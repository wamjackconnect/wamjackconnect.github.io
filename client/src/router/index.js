import Vue from 'vue';
import VueRouter from 'vue-router';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'home',
    component: () => import('../views/HomePage.vue'),
  },
  {
    path: '/registerdev',
    name: 'registerdev',
    component: () => import('../views/Developer/DeveloperRegister.vue'),
  },
  {
    path: '/registercom',
    name: 'registercom',
    component: () => import('../views/Company/CompanyRegister.vue'),
  },
  {
    path: '/logindev',
    name: 'logindev',
    component: () => import('../views/Developer/DeveloperLogin.vue'),
  },
  {
    path: '/logincom',
    name: 'logincom',
    component: () => import('../views/Company/CompanyLogin.vue'),
  },
  {
    path: '/CompanyDash',
    name: 'CompanyDash',
    component: () => import('../views/Company/CompanyDash.vue'),
  },
  {
    path: '/CompanyDash/ProfileEdit',
    name: 'companydashprofile',
    component: () => import('../views/Company/CompanyDash.vue'),
  },
  {
    path: '/CompanyDash/deleteProfile',
    name: 'companydashdelete',
    component: () => import('../views/Company/CompanyDash.vue'),
  },
  {
    path: '/CompanyDash/addContract',
    name: 'companydashaddcontract',
    component: () => import('../views/Company/CompanyDash.vue'),
  },
  {
    path: '/CompanyDash/viewContract',
    name: 'companydashviewcontract',
    component: () => import('../views/Company/CompanyDash.vue'),
  },
  {
    path: '/CompanyDash/ContractApplication',
    name: 'companydashcontractappl',
    component: () => import('../views/Company/CompanyDash.vue'),
  },
  {
    path: '/DeveloperDash',
    name: 'DeveloperDash',
    component: () => import('../views/Developer/DeveloperDash.vue'),
  },
  {
    path: '/DeveloperDash/ProfileEdit',
    name: 'developerdashprofile',
    component: () => import('../views/Developer/DeveloperDash.vue'),
  },
  {
    path: '/DeveloperDash/deleteProfile',
    name: 'developerdashdelete',
    component: () => import('../views/Developer/DeveloperDash.vue'),
  },
  {
    path: '/DeveloperDash/apply',
    name: 'developerdashapply',
    component: () => import('../views/Developer/DeveloperDash.vue'),
  },
  {
    path: '/DeveloperDash/block',
    name: 'developerdashblock',
    component: () => import('../views/Developer/DeveloperDash.vue'),
  },
  {
    path: '/companylogin',
    name: 'Comp Login',
    component: () => import('../views/Company/CompanyLogin.vue'),
  },
  {
    path: '/developerlogin',
    name: 'Dev Login',
    component: () => import('../views/Developer/DeveloperLogin.vue'),
  },
  {
    path: '/companyprofile',
    name: 'profilecom',
    component: () => import('../views/Company/CompanyProfile.vue'),
  },

  {
    path: '/developerprofile',
    name: 'profiledev',
    component: () => import('../views/Developer/DeveloperProfile.vue'),
  },

  {
    path: '/forgotpasswordCom',
    name: 'forgotpasswordCom',
    component: () => import('../views/Company/ForgotPasswordCom.vue'),
  },
  {
    path: '/forgotpasswordDev',
    name: 'forgotpasswordDev',
    component: () => import('../views/Developer/ForgotPasswordDev.vue'),
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

router.afterEach(() => {
  Vue.nextTick(() => {
    document.title = 'Wamjack Connect';
  });
});

export default router;
