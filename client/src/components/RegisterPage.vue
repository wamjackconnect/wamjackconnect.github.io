<!-- The register page serves as a component for the developer and company registration-->
<template>
  <!-- The background colour is assigned from their respective views (dev/comp) -->
  <div class="background">
    <b-container fluid>
      <!-- The page uses a one row and five columns to properly space the elements -->
      <b-row class="dev_row">
        <b-col cols="4"></b-col>
        <b-col id="card-col" cols="4" style="min-width: 40vw">
          <div class="card">
            <b-button
                    variant="link"
                    to="/"
            >
              <b-card-img
                :src="require('../assets/ConnectLogo.png')"
              >
              </b-card-img>
            </b-button>
            <validation-observer ref="observer" v-slot="{ handleSubmit }">
              <!-- Live validation is provided for the input fields by Vee-Validate's provider and
              observer components, as well as bootstrap-vue's live form feedback -->
              <b-form @submit.stop.prevent="handleSubmit(onSubmit)">
                <change-avatar v-model="avatarFile" v-if="!login" @change="change"></change-avatar>
                <validation-provider
                  v-if="!login"
                  name="Name"
                  :rules="{ required: true, min: 3 }"
                  v-slot="validationContext"
                >
                  <b-form-group
                    id="input-group-1"
                  >
                    <b-form-input
                      id="input-1"
                      v-model="form.name"
                      :placeholder="namePlaceholder"
                      :state="getValidationState(validationContext)"
                      class="input_field"
                    ></b-form-input>
                    <b-row class="flex-row">
                      <b-alert
                        variant="danger"
                        fade
                        :show="showUsernameAlert"
                      >Name already exists
                      </b-alert>
                    </b-row>
                    <b-form-invalid-feedback id="input-1-live-feedback">
                      {{ validationContext.errors[0] }}
                    </b-form-invalid-feedback>
                  </b-form-group>
                </validation-provider>
                <validation-provider
                  name="Email"
                  :rules="{ required: true, email: true }"
                  v-slot="validationContext">
                  <b-form-group id="input-group-2">
                    <b-form-input
                      id="input-2"
                      v-model="form.email"
                      placeholder="Enter email"
                      :state="getValidationState(validationContext)"
                      class="input_field"
                    >
                    </b-form-input>
                    <b-alert
                      variant="danger"
                      fade
                      :show="showEmailAlert"
                    >Email already exists
                    </b-alert>
                    <b-form-invalid-feedback id="input-2-live-feedback">
                      {{ validationContext.errors[0] }}
                    </b-form-invalid-feedback>
                  </b-form-group>
                </validation-provider>
                <validation-provider
                  name="Password"
                  :rules="{ required: true, min: 8 }"
                  v-slot="validationContext"
                  vid="confirm"
                >
                  <b-input-group id="input-group-3">
                    <b-form-input
                      id="input-3"
                      placeholder="Password"
                      :type="passwordFieldType"
                      v-model="form.password"
                      :state="getValidationState(validationContext)"
                      class="input_field"
                    ></b-form-input>
                    <b-input-group-append>
                      <b-button variant="success" @click="switchVisibility('password')">
                        Show
                      </b-button>
                    </b-input-group-append>
                    <b-tooltip target="input-3" triggers="hover">
                      Your password must be at least 8 characters long, contain letters and numbers,
                      and must contain at least one special character.
                    </b-tooltip>
                    <b-form-invalid-feedback id="input-3-live-feedback">
                      {{ validationContext.errors[0] }}
                    </b-form-invalid-feedback>
                  </b-input-group>
                  <b-alert
                    variant="danger"
                    :show="showPassAlert"
                  >Incorrect email or password
                  </b-alert>
                </validation-provider>
                <validation-provider
                  v-if="!login"
                  name="confirmPassword"
                  :rules="{ required: true, password: '@confirm' }"
                  v-slot="validationContext"
                >
                  <b-input-group id="input-group-4">
                    <b-form-input
                      id="input-4"
                      placeholder="Confirm Password"
                      :type="confirmFieldType"
                      v-model="form.confirm"
                      :state="getValidationState(validationContext)"
                      class="input_field"
                    ></b-form-input>
                    <b-input-group-append>
                      <b-button variant="success" @click="switchVisibility('confirmPassword')">
                        Show
                      </b-button>
                    </b-input-group-append>
                    <b-form-invalid-feedback id="input-3-live-feedback">
                      Passwords do not match
                    </b-form-invalid-feedback>
                  </b-input-group>
                </validation-provider>
                <multiselect
                  v-if="!login"
                  v-model="selected"
                  label="name"
                  tag-placeholder="Add new tag"
                  :placeholder="multiPlaceholder"
                  track-by="code"
                  :options="options"
                  :multiple="developer"
                  :taggable="true"
                  @tag="addTag"
                  class="input_field"
                ></multiselect>
                <b-form-textarea
                  v-if="!login"
                  id="about"
                  v-model="text"
                  :placeholder="textPlaceholder"
                  max-rows="6"
                  class="input_field mt-2"
                ></b-form-textarea>
                <div style="position: center">
                  <b-button
                    variant="link"
                    :to="routePath">
                    <u>{{ routeText }}</u>
                  </b-button>
                </div>
                <div v-if="login" style="position: center">
                  <b-button
                    variant="link"
                    @click="forgetPassword()">
                    <u>Forgot Password?</u>
                  </b-button>
                </div>
                <b-alert
                  variant="danger"
                  fade
                  :show="showDataAlert"
                >Database error
                </b-alert>
                <b-button
                  id="submit-button"
                  pill
                  type="submit"
                  variant="outline-primary"
                  class="mt-3"
                  :disabled="submitPressed"
                ><b-spinner v-if="submitPressed" small type="grow"></b-spinner>{{ submitText }}
                </b-button>
              </b-form>
            </validation-observer>
          </div>
        </b-col>
        <b-col></b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import Multiselect from 'vue-multiselect';
import { extend } from 'vee-validate';
import axios from 'axios';
import { Modal } from 'bootstrap';
import ChangeAvatar from './form components/changeAvatar.vue';

extend('password', {
  /* Creates a new schema for cross field password validation. Makes it possible to add the confirm
   * password functionality.
   */
  params: ['target'],
  validate(value, { target }) {
    return value === target;
  },
  message: 'Password confirmation does not match',
});

export default {
  name: 'RegisterDevView',
  components: {
    ChangeAvatar,
    Multiselect,
  },
  props: {
    // Defines the props that are passed from DeveloperRegister.vue or CompanyRegister.vue
    login: Boolean,
    developer: Boolean,
    namePlaceholder: String,
    multiPlaceholder: String,
    textPlaceholder: String,
    routerPath: String,
    routerPush: String,
    backgroundProp: String,
    submitText: String,
    options: Array,
    routeText: String,
    routePath: String,
  },
  data() {
    return {
      avatarFile: '',
      email: '',
      context: 'Company',
      form: {
        name: '',
        email: '',
        password: '',
        confirm: '',
      },
      passwordFieldType: 'password',
      confirmFieldType: 'password',
      selected: [],
      text: '',
      showUsernameAlert: false,
      showEmailAlert: false,
      showPassAlert: false,
      showDataAlert: false,
      submitPressed: false,
    };
  },
  methods: {
    forgetPassword() {
      if (this.developer) {
        this.$router.push('/forgotpasswordDev');
      } else {
        this.$router.push('/forgotpasswordCom');
      }
    },
    change() {
      this.avatarFile = 'Changed value';
    },
    getValidationState({ dirty, validated, valid = null }) {
      return dirty || validated ? valid : null;
    },
    async onSubmit() {
      this.submitPressed = true;
      const path = this.routerPath;
      this.showUsernameAlert = false;
      this.showEmailAlert = false;
      this.showPassAlert = false;
      this.showDataAlert = false;

      if (this.login) {
        await axios.post(path, {
          email: this.form.email,
          password: this.form.password,
        }).then((res) => {
          if (res.data[1] === 200) {
            localStorage.token = res.data[0].token;
            if (this.developer) {
              this.$router.push({ name: 'DeveloperDash', params: { jwtToken: res.data[0].token } });
            } else {
              this.$router.push({ name: 'CompanyDash', params: { jwtToken: res.data[0].token } });
            }
          }
          if (res.data[0].message === 'Incorrect password'
            || res.data[0].message === 'User does not exist') {
            this.showPassAlert = true;
            this.submitPressed = false;
          }
          if (res.data[1] === 400) {
            this.showDataAlert = true;
            this.submitPressed = false;
          }
        }).catch((err) => console.log(err));
      } else {
        await axios.post(path, {
          name: this.form.name,
          email: this.form.email,
          password: this.form.password,
          selected: this.selected,
          text: this.text,
          avatar: this.avatarFile,
        }).then((res) => {
          if (res.data[1] === 200) {
            this.$router.push('/');
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
      }
    },
    onClick() {
      this.$forceUpdate();
    },
    switchVisibility(type) {
      if (type === 'password') {
        this.passwordFieldType = this.passwordFieldType === 'password' ? 'text' : 'password';
      } else if (type === 'confirmPassword') {
        this.confirmFieldType = this.confirmFieldType === 'password' ? 'text' : 'password';
      }
    },
    addTag(newTag) {
      const tag = {
        name: newTag,
        code: newTag.substring(0, 2) + Math.floor(Math.random() * 10000000),
      };
      const { options } = this;
      options.push(tag);
      this.value.push(tag);
    },
    mounted() {
      this.modal = new Modal(this.$refs.profileModalfp);
    },
  },
};
</script>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>

<style scoped>

#card-col {
  display: flex;
  justify-content: center;
}

#submit-button:hover {
  transform: scale(110%);
}

.card {
  box-shadow: 0 3px 10px rgb(0 0 0 / 0.2);
  border-radius: 5%;
  padding: 1rem 1rem 1rem 1rem;
  max-width: 400px;
}

.dev_row {
  display: flex;
  min-height: 100vh;
  align-items: center;
}

.input_field {
  margin-bottom: 0.5rem;
  background: inherit;
}

.input_field:focus {
  margin-bottom: 0.5rem;
  transform: scale(105%);
}

.form-control {
  border: 0 solid;
  border-bottom: 1px solid dimgray;
  align-items: end;
}

</style>
