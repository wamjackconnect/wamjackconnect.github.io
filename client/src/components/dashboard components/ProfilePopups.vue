<template>
<div>
  <div class="modal fade" id="ProfileAsDev">
    <div class="modal-dialog modal-dialog-centered modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" v-if = "dataOrigin == 1" >Company Profile as Developer</h5>
          <h5 class="modal-title" v-else-if="dataOrigin == 2">Developer Profile as Company</h5>
          <b-button class="btn-close" data-bs-dismiss="modal" aria-label="Close"></b-button>
        </div>
        <div class="modal-body">
          <b-card>
            <b-row>
              <b-col>
                <b-row>
                  <b-form-group v-if="dataOrigin == 1" class="profile-text">
                    <strong>Company Name</strong>
                    <br>
                    <b-form-text class="mt-3" text-variant="dark">
                      {{ profName }}
                    </b-form-text>
                  </b-form-group>
                  <b-form-group v-else-if="dataOrigin == 2" class="profile-text" >
                    <strong>Username</strong>
                    <br>
                    <b-form-text class="mt-3" text-variant="dark">
                      {{ profName }}
                    </b-form-text>
                  </b-form-group>
                </b-row>
                <b-row>
                  <b-form-group v-if="dataOrigin == 1" class="profile-text">
                    <strong>General Industries</strong>
                    <br>
                    <b-form-text class="mt-3" text-variant="dark">
                      {{ profExtra }}
                    </b-form-text>
                  </b-form-group>
                  <b-form-group v-else-if="dataOrigin == 2" class="profile-text">
                    <strong>Status</strong>
                    <br>
                    <b-form-text class="mt-3" text-variant="dark">
                      {{ profExtra }}
                    </b-form-text>
                  </b-form-group>
                </b-row>
                <b-row>
                  <b-form-group v-if="dataOrigin == 1" class="profile-text">
                    <strong>Description</strong>
                    <br>
                    <b-form-text class="mt-3" text-variant="dark">
                       {{ profDesc }}
                    </b-form-text>
                  </b-form-group>
                  <b-form-group v-else-if="dataOrigin == 2" class="profile-text">
                    <strong>Work Experience</strong>
                    <br>
                    <b-form-text class="mt-3" text-variant="dark">
                       {{ profDesc }}
                    </b-form-text>
                  </b-form-group>
                </b-row>
                <b-row>
                  <b-form-group v-if="dataOrigin == 2" class="profile-text">
                    <strong>Programming Languages</strong>
                    <br>
                    <b-form-text class="mt-3" text-variant="dark">
                       <span v-for="language in profLanguages" :key="language">
                          {{ language.name }}
                          <br>
                        </span>
                    </b-form-text>
                  </b-form-group>
                </b-row>
              </b-col>
              <b-col>
                <b-avatar
                  variant="info"
                  :src="profLogo"
                  size="250">
                </b-avatar>
              </b-col>
            </b-row>
          </b-card>
        </div>
        <div class="modal-footer">
        </div>
      </div>
    </div>
  </div>
  <comEdit v-if="dataOrigin == 1" :token="token" :company-name="profName" :company-email="profEmail"
           :data-origin="1" :company-bio="profDesc" :company-extra="profExtra"
           :company-password="profPassword" :company-logo="profLogo">
  </comEdit>
  <devEdit v-else-if="dataOrigin == 2" :token="token" :username="profName" :email="profEmail"
           :data-origin="2" :bio="profDesc" :extra="profExtra" :password="profPassword"
           :user-avatar="profLogo" :prof-lang="profLanguages">
  </devEdit>
</div>
</template>

<script>
import { Modal } from 'bootstrap';
import comEdit from '@/components/dashboard components/comEdit.vue';
import devEdit from '@/components/dashboard components/devEdit.vue';

export default {
  name: 'ProfilePopups',
  components: {
    comEdit,
    devEdit,
  },
  props: {
    token: String,
    profName: String,
    profEmail: String,
    profPassword: String,
    profLogo: String,
    profDesc: String,
    profExtra: String,
    dataOrigin: Number,
    profLanguages: Array,
  },
  data() {
    return {
      modal: null,
      /* profile: {
        companyName: 'Current Name',
        companyEmail: 'Current Email',
        companyBio: 'Current Bio',
        industry: 'Stuff',
      }, */
    };
  },
  mounted() {
    this.modal = new Modal(this.$refs.ProfileAsDev);
  },
};
</script>

<style scoped>

.profile-text {
  margin: 0 0 1rem 0;
  /*border-bottom: 1px dashed gray;*/
}

.profile-col {
  display: flex;
  width: 100%;
  align-items: center;
  flex-direction: column;
}

.card {
  box-shadow: 0 3px 10px rgb(0 0 0 / 0.2);
  border-radius: 5%;
  padding: 1rem 1rem 1rem 1rem;
  max-width: 100%;
}

</style>
