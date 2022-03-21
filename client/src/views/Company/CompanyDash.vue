<template>
  <div>
    <nav-bar :profile-name="company.CompanyName" :profile-logo="company.Logo"></nav-bar>
    <side-bar :prof-name="company.CompanyName"
              :prof-email="company.Email"
              :prof-logo = "company.Logo"
              :prof-desc = "company.Bio"
              :prof-extra = "company.GeneralIndustry"
              :prof-money = "money_spent"
              :dataOrigin=1></side-bar>
    <ProfilePopups :prof-name="company.CompanyName"
              :prof-email="company.Email"
              :prof-logo = "company.Logo"
              :prof-desc = "company.Bio"
              :prof-extra = "company.GeneralIndustry"
                   :token="this.token"
              :dataOrigin=1></ProfilePopups>
    <b-container fluid id="content-container">
      <b-row class ="row no-pad" style="min-height: 100vh">
        <b-col cols="9" style="background-color: #f1efd7">
            <b-row align-v="center">
              <b-col cols = "2" style="margin-top: 0vh">
                <b-button data-bs-toggle="modal"
                          data-bs-target="#addContract"
                          @click="comDashAddContUrl()">
                  Add Contract
                </b-button>
              </b-col>
              <b-col cols="8"></b-col>
              <b-col>
              <div>
                <b-dropdown id="dropdown-1" text="Sort By" class="m-md-2">
                  <b-dropdown-item @click="sort(0)">All Contracts</b-dropdown-item>
                  <b-dropdown-item @click="sort(1)">Open Contracts</b-dropdown-item>
                  <b-dropdown-item @click="sort(2)">Closed Contracts</b-dropdown-item>
                </b-dropdown>
              </div>
              </b-col>
            </b-row>
            <b-row v-if="sort_id == 0">
              <b-col class="d-flex justify-content-center"
                     cols="4"
                     v-for="contract in contracts_all"
                     :key="contract">
                <contract-card :contract-desc="contract.Descript"
                               :contract-value="contract.Value"
                               :contract-length="contract.Length"
                               :contract-location="contract.Location"
                               :contract-status="contract.Status"
                               :company-logo="company.Logo"
                               :contract-id="contract.ContractID"
                               :contract-languages="contract.PrefLang"
                               @getAppl="getApplications(contract.ContractID)"
                ></contract-card>
              </b-col>
            </b-row>
            <b-row v-else-if="sort_id == 1">
              <b-col class="d-flex justify-content-center"
                     cols="4"
                     v-for="contract in contracts_open"
                     :key="contract">
                <contract-card :contract-desc="contract.Descript"
                               :contract-value="contract.Value"
                               :contract-length="contract.Length"
                               :contract-location="contract.Location"
                               :contract-status="contract.Status"
                               :company-logo="company.Logo"
                               :contract-id="contract.ContractID"
                               :contract-languages="contract.PrefLang"
                               @getAppl="getApplications(contract.ContractID)"
                ></contract-card>
              </b-col>
            </b-row>
            <b-row v-else-if="sort_id == 2">
              <b-col class="d-flex justify-content-center"
                     cols="4"
                     v-for="contract in contracts_closed"
                     :key="contract">
                <contract-card :contract-desc="contract.Descript"
                               :contract-value="contract.Value"
                               :contract-length="contract.Length"
                               :contract-location="contract.Location"
                               :contract-status="contract.Status"
                               :company-logo="company.Logo"
                               :contract-id="contract.ContractID"
                               :contract-languages="contract.PrefLang"
                               @getAppl="getApplications(contract.ContractID)"
                ></contract-card>
              </b-col>
            </b-row>
            <b-row v-else class="loading">
                <h2>Loading Content...</h2>
            </b-row>
        </b-col>
        <b-col cols="3" style="background-color: #bdf6d2">
          <div class="mint">
            <p class = heading >
                  Pending Applications
            </p>
            <div v-if="contrID == null">
              <h6>No Contract Selected</h6>
            </div>
            <div v-else v-for="dev in contrApplicants" :key="dev">
              <developer-cards :dev-name="dev.Username"
                             :dev-email="dev.Email"
                             :dev-experience="dev.Experience"
                             :dev-image="dev.Avatar"
                             :dev-i-d="dev.DeveloperID"
                             :contract-i-d="contrID"
                             :dev-languages="dev.Languages"
                             :status="dev.ApplyStatus"
              ></developer-cards>
            </div>
          </div>
        </b-col>
      </b-row>
      <div class="modal fade" id="addContract" data-bs-backdrop="static" data-bs-keyboard="false">
        <div class="modal-dialog modal-dialog-centered modal-lg">
          <div class="modal-content"
               :style="{ backgroundImage: 'url(' + require('../../assets/ContractForm.png') + ')',
              backgroundSize: 'cover',
              }">
            <div class="modal-header">
              <h5 class="modal-title">Create New Contract</h5>
              <b-button class="btn-close" data-bs-dismiss="modal" aria-label="Close"
                        @click="comDashUrl()">
              </b-button>
            </div>
            <b-row align-v="center">
            <b-col cols="7">
            <div class="modal-body">
              <b-form>
                <b-row class="mt-3">
                    <b-input-group>
                      <b-form-textarea
                        id="edit-com-name"
                        v-model="cont.info"
                        placeholder="Enter contract info..."
                      ></b-form-textarea>
                    </b-input-group>
                </b-row>
                <b-row class="mt-3">
                    <b-input-group prepend="Contract Value">
                      <b-form-input
                        id="input-value"
                        v-model="cont.value"
                        placeholder="Input contract value..."
                        :number="true"
                        :state="valueState"
                      ></b-form-input>
                      <b-form-invalid-feedback id="input-value-feedback">
                        Must be an integer
                      </b-form-invalid-feedback>
                    </b-input-group>
                </b-row>
                <b-row class="mt-3">
                    <b-input-group prepend="Contract Length">
                      <b-form-input
                        id="input-length"
                        v-model="cont.length"
                        placeholder="Enter contract length in months..."
                        :number="true"
                        :state="lengthState"
                      ></b-form-input>
                      <b-form-invalid-feedback id="input-length-feedback">
                        Must be an integer
                      </b-form-invalid-feedback>
                    </b-input-group>
                </b-row>
                <b-row>
                </b-row>
                <b-row class="mt-0">
                    <b-form-group>
                      <multiselect
                        v-model="optionsSelected"
                        label="name"
                        tag-placeholder="Add new tag"
                        placeholder="Select preferred languages..."
                        track-by="code"
                        :options="options"
                        multiple
                        taggable
                        @tag="addTag"
                        class="mt-2 mb-2"
                      ></multiselect>
                        <b-alert
                        variant="danger"
                        fade
                        :show="showPrefAlert"
                      >Please select preferred languages
                      </b-alert>
                    </b-form-group>
                </b-row>
                <b-row>
                  <b-form-group label="Choose the form of location" v-slot="{ ariaDescribedby }">
                    <b-form-radio v-model="selected"
                                  :aria-describedby="ariaDescribedby"
                                  name="some-radios" value="Remote">Remote</b-form-radio>
                    <b-form-radio v-model="selected"
                                  :aria-describedby="ariaDescribedby"
                                  name="some-radios" value="In Office">In Office</b-form-radio>
                  </b-form-group>
                </b-row>
              </b-form>
              <b-button variant="primary" data-bs-dismiss="modal" type="submit"
                        class=topMargin @click="addContrUrl()" >
                Submit
              </b-button>
              </div>
              </b-col>
              <b-col></b-col>
              <b-col cols="4">
                <b-avatar
                      variant="info"
                      :src="company.Logo" size="150"></b-avatar>
              </b-col>
              </b-row>
            </div>
          </div>
      </div>
    </b-container>
  </div>
</template>

<script>
import { Modal } from 'bootstrap';
import Multiselect from 'vue-multiselect';
import axios from 'axios';
import NavBar from '@/components/dashboard components/NavBar.vue';
import SideBar from '@/components/dashboard components/SideBar.vue';
import ProfilePopups from '@/components/dashboard components/ProfilePopups.vue';
import DeveloperCards from '@/components/dashboard components/DeveloperCards.vue';
import ContractCard from '@/components/dashboard components/ContractCard.vue';

export default {
  name: 'CompanyDash',
  components: {
    ContractCard,
    Multiselect,
    DeveloperCards,
    SideBar,
    NavBar,
    ProfilePopups,
  },
  data() {
    return {
      modal: null,
      appliedDevs: null,
      selected: '',
      contrID: null,
      routerPath: 'http://127.0.0.1:5000/CompanyDash',
      token: this.$route.params.jwtToken,
      cont: {
        value: '',
        length: '',
        logo: '',
        info: '',
      },
      company: {},
      contracts_all: {},
      contracts_open: {},
      contracts_closed: {},
      contrApplications: {},
      contrApplicants: {},
      money_spent: 0,
      onViewContr: false,
      sort_id: -1,
      optionsSelected: [],
      options: [
        { code: 'vu', name: 'Vue.js' },
        { code: 'ja', name: 'Java' },
        { code: 'py', name: 'Python' },
        { code: 'ru', name: 'Ruby' },
        { code: 'c++', name: 'C++' },
        { code: 'c', name: 'C' },
      ],

      showPrefAlert: false,
    };
  },
  computed: {
    valueState() {
      if (this.cont.value) {
        // eslint-disable-next-line no-restricted-globals
        if (isNaN(this.cont.value)) return false;
        return null;
      }
      return null;
    },
    lengthState() {
      if (this.cont.length) {
        // eslint-disable-next-line no-restricted-globals
        if (isNaN(this.cont.length)) return false;
        return null;
      }
      return null;
    },
  },
  async mounted() {
    if (localStorage.token) {
      this.token = localStorage.token;
    }
    await this.getCurUser();
    this.modal = new Modal(this.$refs.addContract);
  },
  methods: {
    addTag(newTag) {
      const tag = {
        name: newTag,
        code: newTag.substring(0, 2) + Math.floor(Math.random() * 10000000),
      };
      const { options } = this;
      options.push(tag);
      this.value.push(tag);
    },
    sort(id) {
      this.sort_id = id;
    },
    async addContrUrl() {
      if (Object.keys(this.optionsSelected).length === 0) {
        this.showPrefAlert = true;
        return;
      }
      this.showPrefAlert = false;

      const path = `${this.routerPath}/addContract`;

      await axios.post(path, {
        contractDescr: this.cont.info,
        contractVal: this.cont.value,
        contractLen: this.cont.length,
        prefLang: this.optionsSelected,
        location: this.selected,
      }, {
        headers: {
          tok: this.token,
        },
      }).then((res) => {
        if (res.data[0] === 200) {
          // do something (e.g. update url to show new contract.)
          this.comDashUrl();
          window.location.reload();
        }
      }).catch((err) => console.log(err));
    },
    comDashUrl() {
      this.$router.push('/CompanyDash');
      this.onViewContr = false;
    },
    comDashAddContUrl() {
      this.$router.push({ name: 'companydashaddcontract', params: { jwtToken: this.token } });
      this.onViewContr = false;
    },
    async getApplications(contrID) {
      // TODO: implement requesting list of applications for contract specified by contract_id
      if (!this.onViewContr) {
        // eslint-disable-next-line max-len
        // await this.$router.push({ name: 'companydashviewcontract', params: { jwtToken: this.token } });
        this.onViewContr = true;
      // } else if (contrID === this.contrID) {
      //   this.onViewContr = false;
      //   this.comDashUrl();
      //   this.contrApplications = {};
      //   this.contrApplicants = {};
      //   return;
      }
      this.contrID = contrID;
      const path = `${this.routerPath}/viewContract`;
      const self = this;
      await axios.get(path, {
        headers: {
          contract_id: this.contrID,
        },
      }).then((response) => {
        self.contrApplications = response.data[0].applications;
        self.contrApplicants = response.data[0].applicantDet;
        console.log(response);
      }).catch((err) => {
        console.log(err);
      });
    },
    async getCurUser() {
      const path = this.routerPath;
      const self = this;

      await axios.get(path, {
        headers: {
          tok: this.token,
        },
      }).then((response) => {
        // return to home if not logged in
        if (response.data[1] === 403) {
          this.$router.push('/');
        }
        self.sort_id = 0;
        self.company = response.data[0].CompanyDetails;
        self.contracts_all = response.data[0].Contracts;
        self.contracts_open = response.data[0].OpenContracts;
        self.contracts_closed = response.data[0].ClosedContracts;
        self.money_spent = self.company.MoneySpent;
      }).catch((err) => {
        console.log(err);
      });
    },
  },
};
</script>

<style scoped>
.mint {
   background: #bdf6d2;
}

.cream {
   background: #f1efd7;
}

.loading {
  margin-top: 20px;
  font-style: italic;
  align-content: center;
}

.modal-content {
  height: 500px;
  border-radius: 25px;
}

.modal-content div {
  margin: 0;
}

.row.no-pad {
  margin-left: 0;
  margin-right: 0;
}

.topMargin {
  margin-top: 15px;
}

.row.no-pad > [class*='col-']{
  padding-right: 0;
  padding-left: 0;
}

#content-container {
  margin-left: 0;
  margin-right: 0;
  padding-right: 0;
  padding-left: 0;
}

.heading {
  font-size: 4vh;
  color: #75498D;
}

.conID {
  font-size: larger;
  margin-top: 3vh
}

.bottomCardL{
  background-color: #f1efd7;
  min-height: 85vh;
}
.bottomCardR{
  background-color: #bdf6d2;
  min-height: 85vh;
}

</style>
