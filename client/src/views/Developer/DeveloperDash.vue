<template class="vh-100">
  <div id="div-container">
    <nav-bar :profile-name="developer.Username" :profile-logo="developer.UserAvatar"></nav-bar>
    <side-bar :prof-name="developer.Username"
              :prof-email="developer.Email"
              :prof-logo = "developer.UserAvatar"
              :prof-desc = "developer.Experience"
              :prof-extra = "developer.Status"
              :prof-languages = "developer.Languages"
              :prof-money = "money_made"
              :dataOrigin=2></side-bar>
    <ProfilePopups :prof-name="developer.Username"
                   :prof-email="developer.Email"
                   :prof-logo = "developer.UserAvatar"
                   :prof-desc = "developer.Experience"
                   :prof-extra = "developer.Status"
                   :prof-languages = "developer.Languages"
                   :token="this.token"
                   :dataOrigin=2></ProfilePopups>
    <b-container id="page-container" fluid class="overflow-auto">
      <ContractsTable
        v-if="contr_sort == 0"
        @sortContr="sortContr($event)"
        :is-busy="busyState"
        :contracts = this.contracts
        :rows="contr_rows"
      ></ContractsTable>
      <ContractsTable
        v-else-if="contr_sort == 1"
        @sortContr="sortContr($event)"
        :is-busy="busyState"
        :contracts = this.accepted_contracts
        :rows="acc_rows"
      ></ContractsTable>
      <ContractsTable
        v-if="contr_sort == 2"
        @sortContr="sortContr($event)"
        :is-busy="busyState"
        :contracts = this.pending_contracts
        :rows="pend_rows"
      ></ContractsTable>
    </b-container>
  </div>
</template>

<script>
import NavBar from '@/components/dashboard components/NavBar.vue';
import SideBar from '@/components/dashboard components/SideBar.vue';
import ProfilePopups from '@/components/dashboard components/ProfilePopups.vue';
import axios from 'axios';
import ContractsTable from '@/components/dashboard components/ContractsTable.vue';

export default {
  name: 'DeveloperDash',
  components: {
    ContractsTable,
    SideBar,
    NavBar,
    ProfilePopups,
  },
  data() {
    return {
      token: this.$route.params.jwtToken,
      busyState: true,
      perPage: 3,
      currentPage: 1,
      developer: {},
      contracts: [],
      accepted_contracts: [],
      pending_contracts: [],
      money_made: 0,
      contr_sort: 0,
    };
  },
  computed: {
    contr_rows() {
      return this.contracts.length;
    },
    acc_rows() {
      return this.accepted_contracts.length;
    },
    pend_rows() {
      return this.pending_contracts.length;
    },
  },
  async mounted() {
    if (localStorage.token) {
      this.token = localStorage.token;
    }
    await this.getUser();
  },
  methods: {
    sortContr(key) {
      this.contr_sort = key;
    },
    async getUser() {
      const path = 'http://127.0.0.1:5000/DeveloperDash';
      // const self = this;

      await axios.get(path, {
        headers: {
          tok: this.token,
        },
      }).then((response) => {
        // check if logged in
        if (response.data[1] === 403) {
          this.$router.push('/');
        }
        console.log(response);
        this.developer = response.data[0].developerDetails;
        this.contracts = response.data[0].contracts_dictionary;
        this.accepted_contracts = response.data[0].AcceptedApplications;
        this.pending_contracts = response.data[0].PendingApplications;
        this.money_made = response.data[0].developerDetails.MoneyMade;
        this.busyState = false;
      }).catch((err) => {
        console.log(err);
      });
    },
  },
};
</script>

<style scoped>

#div-container {
  height: 95vh;
}

#page-container {
  height: 100%;
  background: #bdf6d2;
}

</style>
