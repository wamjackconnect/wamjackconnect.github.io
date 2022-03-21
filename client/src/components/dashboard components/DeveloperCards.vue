<template>
  <div v-if="status === 'Accepted'" style="margin-top: 2vh">
    <b-card
      tag="article"
      style="max-width: 30vw;"
      id = "dev-card"
      class="Accepted"
    >
      <b-row>
        <b-col cols="5">
          <b-avatar variant="info" :src="devImage" size="100"></b-avatar>
        </b-col>
        <b-col>
          <br>
          <strong style="font-size: 3vh">{{devName}}</strong> <br>
          {{ status }}
        </b-col>
      </b-row>
      <b-row class="card-body-row">
        <span>
          <strong>Email:</strong> <br>
          {{ devEmail }}
        </span>
      </b-row>
      <b-row class="card-body-row">
        <span>
          <strong>Experience:</strong>
          <br>
          {{ devExperience }}
        </span>
      </b-row>
      <b-row class="card-body-row">
        <strong>Languages:</strong>
        <br>
        <span v-for="language in devLanguages" :key="language">
          {{ language }}
          <br>
        </span>
      </b-row>
      <br>
      <b-row>
      </b-row>
    </b-card>
  </div>
  <div v-else-if="status === 'Declined'" style="margin-top: 2vh">
    <b-card
      tag="article"
      style="max-width: 30vw;"
      class="Declined"
    >
       <b-row>
        <b-col cols="5">
          <b-avatar variant="info" :src="devImage" size="100"></b-avatar>
        </b-col>
        <b-col>
          <br>
          <strong style="font-size: 3vh">{{devName}}</strong> <br>
          {{ status }}
        </b-col>
      </b-row>
      <b-row class="card-body-row">
        <span><strong>Email:</strong> <br>{{ devEmail }}</span>
      </b-row>
      <b-row class="card-body-row">
        <br>
        <span><strong>Experience:</strong> <br> {{ devExperience }}</span>
      </b-row>
      <b-row class="card-body-row">
        <strong>Languages:</strong>
        <br>
        <span v-for="language in devLanguages" :key="language">
          {{ language }}
          <br>
        </span>
      </b-row>
      <b-row>
      </b-row>
    </b-card>
  </div>
  <div v-else-if="status === 'Pending'" >
    <b-card
      tag="article"
      style="max-width: 30vw;"
      class="Pending"
    >
         <b-row>
        <b-col cols="5">
          <b-avatar variant="info" :src="devImage" size="100"></b-avatar>
        </b-col>
        <b-col>
          <br>
          <strong style="font-size: 3vh">{{devName}}</strong> <br>
          {{ status }}
        </b-col>
      </b-row>
      <b-row class="card-body-row">
        <span><strong>Email:</strong> <br> {{ devEmail }}</span>
      </b-row>
      <b-row class="card-body-row">
        <br>
        <span><strong>Experience:</strong> <br> {{ devExperience }}</span>
      </b-row>
      <b-row class="card-body-row">
        <strong>Languages:</strong>
        <br>
        <span v-for="language in devLanguages" :key="language">
          {{ language }}
          <br>
        </span>
      </b-row>
      <b-row>
        <b-col class="card-body-col" cols="6">
          <b-button type="submit" variant="primary" @click="acceptDev()">Accept</b-button>
        </b-col>
        <b-col class="card-body-col">
          <b-button type="submit" variant="danger" @click="declineDev()">Decline</b-button>
        </b-col>
      </b-row>
    </b-card>
  </div>
</template>

<script>

import axios from 'axios';

export default {
  name: 'DeveloperCards',
  props: {
    devName: String,
    devEmail: String,
    devExperience: String,
    devLanguages: Array,
    devImage: String,
    contractID: Number,
    devID: Number,
    status: String,
  },
  data() {
    return {
      modal: null,
      appliedDevs: null,
    };
  },
  methods: {
    async acceptDev() {
      await this.$router.push('/CompanyDash/ContractApplication');
      this.routerPath = 'http://127.0.0.1:5000/CompanyDash/ContractApplication';
      const path = this.routerPath;
      await axios.put(path, {
        // TODO: check variables and finish request.
        ContID: this.contractID,
        DeveloperID: this.devID,
        Accepted: true,
      }).then((res) => {
        if (res.data[0] === 200) {
          // do something (e.g. update url to show new contract.)
        }
      }).catch((err) => console.log(err));
      await this.$router.push('/CompanyDash');
    },
    async declineDev() {
      await this.$router.push('/CompanyDash/ContractApplication');
      this.routerPath = 'http://127.0.0.1:5000/CompanyDash/ContractApplication';
      const path = this.routerPath;
      await axios.put(path, {
        // TODO: check variables and finish request.
        ContID: this.contractID,
        DeveloperID: this.devID,
        Accepted: false,
      }).then((res) => {
        if (res.data[0] === 200) {
          // do something (e.g. update url to show new contract.)
        }
      }).catch((err) => console.log(err));
      await this.$router.push('/CompanyDash');
    },
  },
};
</script>

<style scoped>

#dev-card {
  margin-bottom: 5px;
}

.Accepted {
  background: #8de7a2;
}

.Pending {
  background: #fa58fa;
}

.Declined {
  background: #fc7474;
}

</style>
