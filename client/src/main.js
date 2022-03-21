import { BootstrapVue, IconsPlugin } from 'bootstrap-vue';
import Vue from 'vue';
import {
  extend,
  ValidationObserver,
  ValidationProvider,
} from 'vee-validate';
import * as rules from 'vee-validate/dist/rules';

/* --------------------REGISTER BOOTSTRAP---------------------------------*/
// Import Bootstrap an BootstrapVue CSS files (order is important)
import App from './App.vue';
import router from './router';

import 'vue-multiselect/dist/vue-multiselect.min.css';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';
import '../scss/custom.scss';

// Make BootstrapVue available throughout your project
Vue.use(BootstrapVue);
// Optionally install the BootstrapVue icon components plugin
Vue.use(IconsPlugin);

Object.keys(rules).forEach((rule) => {
  extend(rule, rules[rule]);
});
Vue.component('ValidationObserver', ValidationObserver);
Vue.component('ValidationProvider', ValidationProvider);
/*-----------------------------------------------------------------------*/

Vue.config.productionTip = false;

new Vue({
  router,
  render: (h) => h(App),
}).$mount('#app');
