<template>
  <div>
    <div class="modal fade" id="devEdit" data-bs-backdrop="static"
       data-bs-keyboard="false">
    <div class="modal-dialog modal-dialog-centered modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Edit Profile</h5>
          <b-button @click="devDashUrl()" class="btn-close" data-bs-dismiss="modal"
                    aria-label="Close">
          </b-button>
        </div>
        <div class="modal-body">
          <b-form @submit="devEdit">
            <change-avatar v-model="profile.Avatar" :url="UserAvatar" @change="change">
            </change-avatar>
            <b-row class="mt-3">
              <b-col></b-col>
              <b-col cols="6">
                <b-input-group prepend="Username">
                  <b-form-input
                    id="input-1"
                    v-model="profile.Username"
                    placeholder="Enter a new username..."
                    type="text"
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
                <b-input-group prepend="Email">
                  <b-form-input
                    id="input-2"
                    v-model="profile.Email"
                    placeholder="Enter a new email..."
                    type="email"
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
                <b-form-text class="mt-0" text-variant="dark">Status
                </b-form-text>
              </b-col>
              <b-col cols="5">
                <multiselect
                  id="input-3"
                  v-model="profile.Status"
                  label="name"
                  placeholder="Select status..."
                  :options="statusOptions"
                  class="mt-2"
                >
                </multiselect>
              </b-col>
              <b-col></b-col>
            </b-row>
            <b-row class="mt-0">
              <b-col></b-col>
              <b-col cols="1" align-self="center">
                <b-form-text class="mt-0" text-variant="dark">Languages
                </b-form-text>
              </b-col>
              <b-col cols="5">
                <multiselect
                  v-model="profile.Languages"
                  placeholder="Select Programming Languages..."
                  label="name"
                  track-by="name"
                  :multiple="true"
                  :taggable="true"
                  :options="languageOptions"
                  class="mt-2"
                  @tag="addTag"
                >
                </multiselect>
              </b-col>
              <b-col></b-col>
            </b-row>
            <b-row class="mt-3">
              <b-col></b-col>
              <b-col cols="6">
                <b-input-group>
                  <b-form-textarea
                    id="edit-dev-bio"
                    v-model="profile.Bio"
                    placeholder="Give a short description of your programming
                    language expertise..."
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
          <b-button variant="danger" data-bs-target="#deleteUser"
                     data-bs-toggle="modal" data-bs-dismiss="modal">
            Delete Account
          </b-button>
          <b-button @click="devDashUrl()" variant="secondary" data-bs-dismiss="modal">
            Cancel
          </b-button>
          <b-button @click="devEdit()" variant="primary" type="submit"
                    :disabled="submitPressed">
            <b-spinner v-if="submitPressed" small type="grow"></b-spinner>
            Confirm
          </b-button>
          <!-- <b-button variant="primary" data-bs-dismiss="modal">Close</b-button> -->
        </div>
      </div>
    </div>
  </div>
  <div class="modal fade" id="deleteUser" data-bs-backdrop="static" data-bs-keyboard="false">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <strong>Warning!</strong>
        </div>
        <div class="modal-body">
          <h3><strong>Are you sure you want to delete your account?</strong></h3>
        </div>
        <div class="modal-footer">
          <b-button variant="danger" @click="deleteProfile()" data-bs-dismiss="modal">Yes</b-button>
          <b-button variant="secondary" @click="devDashUrl()" data-bs-dismiss="modal">
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
    Username: {
      deep: true,
      // eslint-disable-next-line
      handler: function (newVal, oldVal) {
        this.profile.Username = newVal;
      },
    },
    Email: {
      deep: true,
      // eslint-disable-next-line
      handler: function (newVal, oldVal) {
        this.profile.Email = newVal;
      },
    },
    UserAvatar: {
      deep: true,
      // eslint-disable-next-line
      handler: function (newVal, oldVal) {
        this.profile.Avatar = newVal;
      },
    },
    Bio: {
      deep: true,
      // eslint-disable-next-line
      handler: function (newVal, oldVal) {
        this.profile.Bio = newVal;
      },
    },
    Status: {
      deep: true,
      // eslint-disable-next-line
      handler: function (newVal, oldVal) {
        this.profile.Status = newVal;
      },
    },
    profLang: {
      deep: true,
      // eslint-disable-next-line
      handler: function (newVal, oldVal) {
        this.profile.Languages = newVal;
      },
    },
  },
  props: {
    token: String,
    Username: String,
    Email: String,
    Password: String,
    UserAvatar: String,
    Bio: String,
    Extra: String,
    dataOrigin: Number,
    profLang: Array,
  },
  data() {
    return {
      modal: null,
      profile: {
        Username: this.Username,
        Email: this.Email,
        Bio: this.Bio,
        Status: this.Extra,
        Avatar: this.UserAvatar,
        Languages: this.profLang,
      },
      edit: {
        Username: '',
        Email: '',
        Experience: '',
        Status: '',
        Avatar: '',
        Languages: [],
      },
      statusOptions: [
        { name: 'Available' },
        { name: 'Unavailable' },
      ],
      languageOptions: [
        { name: 'Vue.js' },
        { name: 'Java' },
        { name: 'Python' },
        { name: 'Ruby' },
        { name: 'C++' },
        { name: 'C' },
      ],
      showUsernameAlert: false,
      showEmailAlert: false,
      showPassAlert: false,
      showDataAlert: false,
      submitPressed: false,
    };
  },
  mounted() {
    this.modal = new Modal(this.$refs.devProfileEdit);
    this.modal = new Modal(this.$refs.deleteUser);
  },
  methods: {
    change(value) {
      this.profile.Avatar = value;
    },
    devDashUrl() {
      this.$router.push('/DeveloperDash');
    },
    getValidationState({ dirty, validated, valid = null }) {
      return dirty || validated ? valid : null;
    },
    async devEdit() {
      this.routerPath = 'http://127.0.0.1:5000/DeveloperDash/profileEdit';
      const path = this.routerPath;
      this.submitPressed = true;
      this.showUsernameAlert = false;
      this.showEmailAlert = false;
      this.showPassAlert = false;
      this.showDataAlert = false;
      await axios.put(path, {
        Username: this.profile.Username,
        Email: this.profile.Email,
        Status: this.profile.Status,
        Experience: this.profile.Bio,
        Avatar: this.profile.Avatar,
        Languages: this.profile.Languages,
      }, {
        headers: {
          tok: this.token,
        },
      }).then(async (res) => {
        console.log(res);
        if (res.data[1] === 200) {
          this.devDashUrl();
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
        // await this.$router.push({ name: 'DeveloperDashDash', params: { jwtToken: this.token } });
      }).catch((err) => console.log(err));
    },
    async deleteProfile() {
      // TODO: post request to delete company account (url switches above)
      await this.$router.push('/DeveloperDash/deleteProfile');
      const path = 'http://127.0.0.1:5000/DeveloperDash/deleteProfile';
      await axios.delete(path, {
        // TODO: check variables and finish request.
        headers: {
          tok: this.token,
        },
      }).then((res) => {
        console.log(res);
        if (res.data[0] === 200) {
          // do something (e.g. update url to show new contract.)
        }
      }).catch((err) => console.log(err));
      await this.$router.push('/');
    },
    addTag(newTag) {
      const tag = {
        name: newTag,
      };
      const { options } = this;
      options.push(tag);
      this.value.push(tag);
    },
  },
};
</script>

<style scoped>

</style>
