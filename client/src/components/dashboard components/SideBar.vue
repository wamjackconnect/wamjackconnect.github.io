<template>
    <div>
      <b-sidebar id="sidebar-1" :title="profName" shadow width="420px">
        <div class="text-start" style="margin-left: 15px">
        <strong v-if="dataOrigin == 1" > Money Spent: </strong>
            <strong v-else-if="dataOrigin == 2">Money Made: </strong>
          R{{ profMoney }}
            <br>
        </div>
        <div class="px-3 py-2">
          <b-avatar variant="info" :src="profLogo" size="150"></b-avatar>
          <br><br>
          <p>
            <strong v-if="dataOrigin == 1" >Company Name</strong>
            <strong v-else-if="dataOrigin == 2">Developer Name</strong>
            <br>
            {{ profName }}
            <br style="margin-bottom: 15px">
            <strong v-if="dataOrigin == 1">Company Email</strong>
            <strong v-else-if="dataOrigin == 2">Email</strong>
            <br>
            {{ profEmail }}
            <br style="margin-bottom: 15px">
            <strong v-if="dataOrigin == 1">General Industries</strong>
            <strong v-else-if="dataOrigin == 2">Status</strong>
            <br>
            {{ profExtra }}
            <br style="margin-bottom: 15px">
            <strong v-if="dataOrigin == 1">Company Description</strong>
            <strong v-else-if="dataOrigin == 2">Work Experience</strong>
            <br>
            {{ profDesc }}
            <br style="margin-bottom: 15px">
            <strong v-if="dataOrigin == 2">Programming Languages</strong>
            <br v-if="dataOrigin == 2">
            <span v-for="language in profLanguages" :key="language">
              {{ language.name }}
              <br>
            </span>
          </p>
        </div>
        <div class="footer">
          <b-button v-if="dataOrigin == 1" data-bs-toggle="modal"
                    variant="primary" data-bs-target="#comEdit">
            Edit Profile
          </b-button>
          <b-button v-else-if="dataOrigin == 2" data-bs-toggle="modal"
                    variant="primary" data-bs-target="#devEdit">
            Edit Profile
          </b-button>
          <b-button v-if="dataOrigin == 1" data-bs-toggle="modal" variant="secondary"
                    data-bs-target="#ProfileAsDev">
              View as Developer
          </b-button>
          <b-button v-else-if="dataOrigin == 2" data-bs-toggle="modal" variant="secondary"
                    data-bs-target="#ProfileAsDev">
              View as Company
          </b-button>
        </div>
      </b-sidebar>
    </div>
</template>

<script>
// src="../../router/index.js"
export default {
  name: 'SideBar',
  props: {
    profName: String,
    profEmail: String,
    profPassword: String,
    profLogo: String,
    profDesc: String,
    profExtra: String,
    dataOrigin: Number,
    profMoney: Number,
    profLanguages: Array,
  },
  /* data() {
    return {
      profile: {
        companyName: 'Current Name',
        companyBio: 'Current Bio',
        industry: 'Stuff',
      },
    };
  }, */
  methods: {
    // Change url on Edit Profile button Click
    // TODO: any post request from this url associated with updating Profile
  },
};
</script>

<style scoped>

</style>
