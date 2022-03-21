<template>
  <div id="div-size">
    <b-card
      tag="article"
      class="m-3 card-container"
      @click="toggleDetails"
      id="card"
    >
        <b-row>
          <b-col id="logo" cols="3">
          <b-avatar variant="info" :src="companyLogo" size="70"></b-avatar>
          </b-col>
        </b-row>
        <b-card-text>
          Status: {{ contractStatus }}
          <br>
          {{ contractDesc }}
        </b-card-text>
        <b-row align-v="end">
          <b-col>
            <b-button variant="tertiary" @click="viewContr()"
                      class="stretched-link" id="selectContr">
            </b-button>
          </b-col>
        </b-row>
      <b-collapse :id="this.contractId">
        <b-card id="contractDetails">
          <b-container fluid>
            <b-row>
              <b-col class="contrDet" cols="2">
                <span><strong>Length:</strong><br>{{ contractLength }} Months</span>
              </b-col>
              <b-col class="contrDet" cols="2">
                <span><strong>Location:</strong><br>{{ contractLocation }}</span>
              </b-col>
            </b-row>
            <b-row>
              <b-col class="contrDet" cols="2">
                <span><strong>Languages:</strong></span>
                <br>
                <span v-for="lang in contractLanguages" :key="lang">
                  {{ lang }}<br>
                </span>
              </b-col>
              <b-col id="card-value" class="contrDet">
                <span><strong>Value:</strong><br>R{{ contractValue }}</span>
              </b-col>
            </b-row>
          </b-container>
        </b-card>
      </b-collapse>
    </b-card>
  </div>
</template>

<script>

export default {
  name: 'ContractCard',
  props: {
    contractDesc: String,
    contractValue: Number,
    companyLogo: String,
    contractLength: String,
    contractStatus: String,
    contractLocation: String,
    contractId: Number,
    contractLanguages: Array,
    dataOrigin: Number,
  },
  data() {
    return {
    };
  },
  mounted() {
  },
  methods: {
    toggleDetails() {
      this.$root.$emit('bv::toggle::collapse', this.contractId);
      // this.$emit('getAppl');
    },
    viewContr() {
      // TODO: pair this with GET request for contract info
      // TODO: Can also expect POST request to accept/decline
      this.$emit('getAppl');
    },
  },
};
</script>

<style scoped>
#logo {
  justify-content: left;
}

#card-value {
  text-align: center;
}

.contrDet {
  width: 45%;
  text-align: center;
  margin: 0;
  padding: 5px 0px;
}

#div-size {
  width: 100%;
}

#contractDetails {
  border: none;
}

.card-container {
  background-image: url('../../assets/ContractCard.png');
  background-size: auto;
  width: 100%;
  height: auto;
  box-shadow: 0 3px 5px rgb(0 0 0 / 0.2);
  border-radius: 5%;
  border: 0 none #FFFFFF;
}

.card-container:hover {
  transform: scale(101%);
  box-shadow: 0 4px 10px rgb(0 0 0 / 0.2);
}

.card-container:focus {
  transform: scale(101%);
  box-shadow: 0 4px 10px rgb(0 0 0 / 0.2);
}

#card {
  max-width: 21vw;
}

#selectContr:focus {
  outline: none;
  box-shadow: none;
}

</style>
