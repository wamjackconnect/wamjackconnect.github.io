<template>
  <b-container id="table-container" fluid>
    <b-row class="row-padding"></b-row>
    <b-row id="table-row" class="align-items-center">
      <b-col cols="4" id="options-col" class="align-self-start">
        <b-card id="options-card">
          <b-form-group
            label="Filter"
            label-for="filter-input"
            label-cols-sm="3"
            label-align-sm="right"
            label-size="sm"
            class="mb-0"
          >
            <b-input-group size="sm">
              <b-form-input
                id="filter-input"
                v-model="filter"
                type="search"
                placeholder="Type to Search"
              ></b-form-input>
              <b-input-group-append>
                <b-button :disabled="!filter" @click="filter = ''">Clear</b-button>
              </b-input-group-append>
            </b-input-group>
          </b-form-group>
          <b-form-group label="Location" class="mt-3">
            <b-form-radio v-model="filter"
                          name="location"
                          value="Remote"
                          class="d-inline m-2"
            >
              Remote
            </b-form-radio>
            <b-form-radio v-model="filter"
                          name="location"
                          value="In Office"
                          class="d-inline m-2"
            >
              In Office
            </b-form-radio>
          </b-form-group>
          <b-form-group
            :v-model="sortDirection"
            label="Filter On"
            description="Leave all unchecked to filter on all data"
            label-cols-sm="3"
            label-align-sm="right"
            label-size="sm"
            class="mb-0"
            v-slot="{ ariaDescribedby }"
          >
            <b-form-checkbox-group
              v-model="filterOn"
              :aria-describedby="ariaDescribedby"
              class="mt-1"
            >
              <b-form-checkbox value="CompanyName" class="d-inline m-2">
                CompanyName
              </b-form-checkbox>
              <b-form-checkbox value="PrefLang" class="d-inline m-2">
                Preferred Languages
              </b-form-checkbox>
            </b-form-checkbox-group>
          </b-form-group>
          <b-form-group
            label="Per page"
            label-for="per-page-select"
            label-cols-sm="6"
            label-cols-md="4"
            label-cols-lg="3"
            label-align-sm="right"
            label-size="sm"
            class="mb-0"
          >
            <b-form-select
              id="per-page-select"
              v-model="perPage"
              :options="pageOptions"
              size="sm"
            ></b-form-select>
          </b-form-group>
          <b-dropdown id="dropdown-1" text="Contracts to show" class="m-md-2">
            <b-dropdown-item @click="sort(0)">All Contracts</b-dropdown-item>
            <b-dropdown-item @click="sort(1)">Accepted Contracts</b-dropdown-item>
            <b-dropdown-item @click="sort(2)">Pending Contracts</b-dropdown-item>
          </b-dropdown>
        </b-card>
      </b-col>
      <b-col cols="8" class="align-self-start">
        <b-table
          ref="table"
          :items="contracts"
          :fields="fields"
          :current-page="currentPage"
          :per-page="perPage"
          :filter="filter"
          :filter-included-fields="filterOn"
          :sort-by.sync="sortBy"
          :sort-desc.sync="sortDesc"
          :sort-direction="sortDirection"
          :hover="true"
          :bordered="true"
          :busy="isBusy"
          sticky-header
          :tbody-tr-class="rowClass"
          selectable
          select-mode="single"
          thead-tr-class="table-primary"
          stacked="md"
          show-empty
          small
          @filtered="onFiltered"
        >
          <template #table-busy>
            <div class="text-center text-danger my-2">
              <b-spinner class="align-middle"></b-spinner>
              <strong>Loading Contracts...</strong>
            </div>
          </template>
          <template #cell(Selected)="row">
            <b-button variant="primary" size="sm" @click="row.toggleDetails">
              {{ row.detailsShowing ? 'Hide' : 'Show' }}
            </b-button>
          </template>
          <template #cell(PrefLang)="row">
            <div v-for="language in row.item.PrefLang"
                 :key="language"
                 class="d-inline">
              {{ language.name }}
            </div>
          </template>
          <template #row-details="row">
            <b-card
              id="dropdownCard"
              :header="row.item.CompanyName"
              header-bg-variant="light"
              header-border-variant="light"
            >
              <b-card-body>
                <b-row align-content="center" align-v="center">
                  <b-col cols="6">
                    <b-avatar
                      variant="info"
                      :src="row.item.CompanyLogo"
                      size="8rem"
                    >
                    </b-avatar>
                  </b-col>
                  <b-col cols="6">
                    <b-card id="descriptionCard">
                      {{ row.item.Descript }}
                    </b-card>
                  </b-col>
                </b-row>
                <b-button variant="success"
                          class="mt-3"
                          @click="apply(row.item.ContractID)"
                          :disabled="disableButtons"
                >
                  Apply
                </b-button>
              </b-card-body>
              <b-card-footer footer-bg-variant="light">
                <b-button variant="link"
                          @click="block(row.item.CompanyName)"
                          class="text-danger"
                          :disabled="disableButtons"
                >
                  Click here to block company!
                </b-button>
              </b-card-footer>
            </b-card>
          </template>
        </b-table>
        <b-pagination
          v-model="currentPage"
          :total-rows="rows"
          :per-page="perPage"
          first-number
          last-number
          align="center"
          size="lg"
          class="my-0"
          pills
        ></b-pagination>
      </b-col>
    </b-row>
    <b-row class="row-padding"></b-row>
  </b-container>
</template>

<script>

import axios from 'axios';

export default {
  name: 'ContractsTable',
  props: {
    contracts: Array,
    isBusy: Boolean,
  },
  data() {
    return {
      totalRows: 1,
      perPage: 10,
      currentPage: 1,
      pageOptions: [5, 10, 15, { value: 100, text: 'Show a lot' }],
      sortBy: '',
      sortDesc: false,
      sortDirection: 'asc',
      filter: null,
      filterOn: [],
      fields: [
        {
          key: 'Selected', label: 'Details',
        },
        {
          key: 'CompanyName',
          label: 'Company Name',
        },
        {
          key: 'PrefLang',
          label: 'Preferred Languages',
        },
        {
          key: 'CompanyEmail',
          label: 'Company Email',
          sortable: true,
          thClass: 'd-none',
          tdClass: 'd-none',
        },
        {
          key: 'CompanyLogo',
          label: 'Company Logo',
          sortable: true,
          thClass: 'd-none',
          tdClass: 'd-none',
        },
        {
          key: 'Length', label: 'Length (months)', sortable: true, class: 'text-center',
        },
        {
          key: 'Location', label: 'Location', sortable: false, class: 'text-center',
        },
        {
          key: 'DatePost', label: 'Date Created', sortable: true, class: 'text-center',
        },
        {
          key: 'Value', label: 'Value', sortable: true, class: 'text-center',
        },
        {
          key: 'Status', label: 'Status', sortable: false,
        },
      ],
      disableButtons: false,
    };
  },
  computed: {
    sortOptions() {
      return this.fields
        .filter((f) => f.sortable)
        .map((f) => ({ text: f.label, value: f.key }));
    },
    rows() {
      return this.contracts.length;
    },
  },
  methods: {
    sort(key) {
      this.$emit('sortContr', key);
    },
    onFiltered(filteredItems) {
      // Trigger pagination to update the number of buttons/pages due to filtering
      this.totalRows = filteredItems.length;
      this.currentPage = 1;
    },
    rowClass(contract, type) {
      if (contract && type === 'row') {
        if (contract.Status === 'Closed') return 'table-secondary';
      }
      return 'table-primary';
    },
    showDetails() {
      this.$refs.table.selectRow();
    },
    apply(ContractID) {
      const path = 'http://127.0.0.1:5000/DeveloperDash';
      this.disableButtons = true;

      console.log(ContractID);
      console.log(localStorage.token);
      axios.post(path, {
        id: ContractID,
        operation: 1, // Apply
      }, {
        headers: {
          tok: localStorage.token,
        },
      }).then((response) => {
        if (response.data[1] === 200) {
          window.location.reload();
        }
        console.log(response);
      }).catch((err) => {
        console.log(err);
      });
    },
    block(CompanyName) {
      const path = 'http://127.0.0.1:5000/DeveloperDash';
      this.disableButtons = true;

      axios.post(path, {
        company: CompanyName,
        operation: 0, // Block
      }, {
        headers: {
          tok: localStorage.token,
        },
      }).then((response) => {
        if (response.data[1] === 200) {
          window.location.reload();
        }
        console.log(response);
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

.complement {
  background: #e2d1dc;
}

#options-col {
}

#options-card {
  height: 90%;
  border-radius: 5%;
}

#descriptionCard {
  vertical-align: center;
  height: 8rem;
  border-radius: 3%;
}

#dropdownCard {
  background: #a1d9d7;
  max-width: 30rem;
  border-radius: 3%;
  border: none;
}

#dropdownCard:hover {
  transform: scale(101%);
  box-shadow: 0 2px 5px rgb(0 0 0 / 0.2);
}

#table-container {
  height: 100%;
  width: 100%;
}

#table-row {
  height: 100%;
}

.row-padding {
  height: 5%;
}

</style>
