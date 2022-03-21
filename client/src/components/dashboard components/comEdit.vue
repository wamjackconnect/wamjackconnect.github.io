<template>
  <div>
    <div class="modal fade" id="comEdit" data-bs-backdrop="static"
       data-bs-keyboard="false">
    <div class="modal-dialog modal-dialog-centered modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Edit Company Profile</h5>
          <b-button @click="comDashUrl()" class="btn-close" data-bs-dismiss="modal"
                    aria-label="Close">
          </b-button>
        </div>
        <div class="modal-body">
          <b-form @submit="onSubmit">
            <change-avatar v-model="profile.comLogo" :url="companyLogo" @change="change($event)">
            </change-avatar>
            <b-row class="mt-3">
              <b-col></b-col>
              <b-col cols="6">
                <b-input-group prepend="Company Name">
                  <b-form-input
                    id="input-1"
                    v-model="profile.comName"
                    placeholder="Enter new company name..."
                  ></b-form-input>
                  <b-row class="flex-row">
                    <b-alert
                      variant="danger"
                      fade
                      :show="showUsernameAlert"
                    >Name already exists
                    </b-alert>
                  </b-row>
                </b-input-group>
              </b-col>
              <b-col></b-col>
            </b-row>
            <b-row class="mt-3">
              <b-col></b-col>
              <b-col cols="6">
                <b-input-group prepend="Company Email">
                  <b-form-input
                    id="input-2"
                    v-model="profile.comEmail"
                    placeholder="Enter new company email..."
                  ></b-form-input>
                  <b-alert
                    variant="danger"
                    fade
                    :show="showEmailAlert"
                  >Email already exists
                  </b-alert>
                </b-input-group>
              </b-col>
              <b-col></b-col>
            </b-row>
            <b-row>
            </b-row>
            <b-row class="mt-0">
              <b-col></b-col>
              <b-col cols="1" align-self="center">
                <b-form-text class="mt-0" text-variant="dark" style="font-size: 1.5vh">Industries
                </b-form-text>
              </b-col>
              <b-col cols="5">
                <multiselect
                  class="mt-2"
                  v-model="profile.comIndustry"
                  label="name"
                  placeholder="Select General Industry..."
                  :options="indusOptions"
                ></multiselect>
              </b-col>
              <b-col></b-col>
            </b-row>
            <b-row>
              <b-form-text class="mt-2" text-variant="dark" style="font-size: 1.8vh"
              >Description</b-form-text>
            </b-row>
            <b-row class="mt-1">
              <b-col></b-col>
              <b-col cols="6">
                <b-input-group>
                  <b-form-textarea
                    id="edit-com-bio"
                    v-model="profile.comBio"
                    placeholder="Give a short description of your company and its goals..."
                  ></b-form-textarea>
                </b-input-group>
              </b-col>
              <b-col></b-col>
            </b-row>
            <b-alert
              variant="danger"
              fade
              :show="showDataAlert"
            >Database error
            </b-alert>
          </b-form>
        </div>
        <div class="modal-footer">
          <b-button variant="danger" data-bs-target="#deleteCompany"
                     data-bs-toggle="modal" data-bs-dismiss="modal">
            Delete Account
          </b-button>
          <b-button @click="comDashUrl()" variant="secondary" data-bs-dismiss="modal">
            Cancel
          </b-button>
          <b-button @click="comEdit()" variant="primary" type="submit"
                    :disabled="submitPressed">
            <b-spinner v-if="submitPressed" small type="grow"></b-spinner>
            Confirm
          </b-button>
          <!-- <b-button variant="primary" data-bs-dismiss="modal">Close</b-button> -->
        </div>
      </div>
    </div>
  </div>
  <div class="modal fade" id="deleteCompany" data-bs-backdrop="static" data-bs-keyboard="false">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <strong>Warning!</strong>
        </div>
        <div class="modal-body">
          <h3><strong>Are you sure you want to delete your account?</strong></h3>
        </div>
        <div class="modal-footer">
          <b-button variant="danger" @click="onDelete()" data-bs-dismiss="modal">Yes</b-button>
          <b-button variant="secondary" @click="comDashUrl()" data-bs-dismiss="modal">
            No
          </b-button>
        </div>
      </div>
    </div>
  </div>
  </div>
</template>

<script>
import { Modal } from 'bootstrap';
import Multiselect from 'vue-multiselect';
import axios from 'axios';
import ChangeAvatar from '../form components/changeAvatar.vue';

export default {
  name: 'ProfilePopups',
  components: {
    ChangeAvatar,
    Multiselect,
  },
  watch: {
    companyName: {
      deep: true,
      // eslint-disable-next-line
      handler: function (newVal, oldVal) {
        this.profile.comName = newVal;
      },
    },
    companyEmail: {
      deep: true,
      // eslint-disable-next-line
      handler: function (newVal, oldVal) {
        this.profile.comEmail = newVal;
      },
    },
    companyLogo: {
      deep: true,
      // eslint-disable-next-line
      handler: function (newVal, oldVal) {
        this.profile.comLogo = newVal;
      },
    },
    companyBio: {
      deep: true,
      // eslint-disable-next-line
      handler: function (newVal, oldVal) {
        this.profile.comBio = newVal;
      },
    },
    companyExtra: {
      deep: true,
      // eslint-disable-next-line
      handler: function (newVal, oldVal) {
        this.profile.comIndustry = newVal;
        this.reRender();
      },
    },
  },
  props: {
    token: String,
    companyName: String,
    companyEmail: String,
    companyPassword: String,
    companyLogo: String,
    companyBio: String,
    companyExtra: String,
    dataOrigin: Number,
  },
  data() {
    return {
      renderKey: 0,
      modal: null,
      avatarFile: '',
      profile: {
        comName: this.companyName,
        comEmail: this.companyEmail,
        comBio: this.companyBio,
        comIndustry: this.companyExtra,
        comLogo: this.companyLogo,
      },
      selected: this.companyExtra,
      indusOptions: [
        { name: 'Games' },
        { name: 'News' },
        { name: 'Software' },
        { name: 'Social Media' },
        { name: 'Security' },
        { name: 'Logistics' },
      ],
      showUsernameAlert: false,
      showEmailAlert: false,
      showPassAlert: false,
      showDataAlert: false,
      submitPressed: false,
    };
  },
  mounted() {
    this.modal = new Modal(this.$refs.comProfileEdit);
    this.modal = new Modal(this.$refs.deleteCompany);
  },
  methods: {
    reRender() {
      this.renderKey += 1;
    },
    onSubmit() {
    },
    change(value) {
      this.profile.logo = value;
    },
    comDashUrl() {
      this.$router.push('/CompanyDash');
    },
    async onDelete() {
      await this.$router.push('/CompanyDash/deleteProfile');
      const path = 'http://127.0.0.1:5000/CompanyDash/deleteProfile';
      await axios.delete(path, {
        // TODO: check variables and finish request.
        headers: {
          tok: this.token,
        },
      }).then((res) => {
        console.log(res);
        if (res.data[0] === 200) {
          // success
        }
      }).catch((err) => console.log(err));
      await this.$router.push('/');
    },
    async comEdit() {
      this.routerPath = 'http://127.0.0.1:5000/CompanyDash/profileEdit';
      const path = this.routerPath;
      this.submitPressed = true;
      this.showUsernameAlert = false;
      this.showEmailAlert = false;
      this.showPassAlert = false;
      this.showDataAlert = false;
      await axios.put(path, {
        CompanyName: this.profile.comName,
        Email: this.profile.comEmail,
        GeneralIndustry: this.profile.comIndustry,
        Bio: this.profile.comBio,
        Avatar: this.profile.comLogo,
      }, {
        headers: {
          tok: this.token,
        },
      }).then((res) => {
        console.log(res);
        if (res.data[1] === 200) {
          this.comDashUrl();
          window.location.reload();
        }
        if (res.data[0].message === 'Email already exists.') {
          this.showEmailAlert = true;
          this.submitPressed = false;
        }
        if (res.data[0].message === 'Name already exists.') {
          this.showUsernameAlert = true;
          this.submitPressed = false;
        }
        if (res.data[1] === 400) {
          this.showDataAlert = true;
          this.submitPressed = false;
        }
      }).catch((err) => console.log(err));
    },
  },
};
</script>

<style scoped>

</style>
