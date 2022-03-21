<template>
  <div>
    <b-container fluid>
      <b-row>
          <b-navbar id="nav" toggleable="lg" type="dark" variant="secondary">
      <b-col cols="1" id="nav-profile">
          <avatar-button :prof-logo="profileLogo" v-b-toggle.sidebar-1></avatar-button>
      </b-col>
      <b-col cols="2" id="brand">
          <b-navbar-brand disabled>{{ profileName }}</b-navbar-brand>
      </b-col>
      <b-col cols="7">
        <img
        alt="Connect logo"
        src= '../../assets/WamjackLogo.png'
        height="60px">
      </b-col>
      <b-col cols="2" id="home-button">
        <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
        <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav>
          <b-nav-item @click="logout" to="/">Sign out</b-nav-item>
        </b-navbar-nav>
        </b-collapse>
      </b-col>
          </b-navbar>
      </b-row>
    </b-container>
</div>

</template>

<script>
import AvatarButton from '@/components/dashboard components/AvatarButton.vue';

export default {
  name: 'NavBar',
  components: { AvatarButton },
  props: {
    profileName: String,
    profileLogo: String,
  },
  methods: {
    logout() {
      localStorage.token = null;
    },
  },
};
</script>

<style scoped>
.mint {
   background: #cbfffa;
}

.cream {
   background: #eedecf;
}

#nav-profile {
  width: 75px;
}

#brand {
  text-align: left;
}

#home-button {
  justify-content: right;
}

#nav-collapse {
  justify-content: right;
}

#nav {
   height:60px
}

</style>
