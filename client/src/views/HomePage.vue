<template>
    <div :style="{ backgroundImage: 'url(' + require('../assets/HomeBackground.png') + ')',
              backgroundPosition: 'center center',
              backgroundSize: '100 100',
              }" id="background">
      <img
        alt="Connect logo"
        src= '../assets/ConnectLogo.png'>
       <b-container fluid :style="{ backgroundImage: 'url(' +
       require('../assets/HomeBackground.png') + ')',
              backgroundPosition: 'center center',
              backgroundSize: '100 100',
              }">
        <b-row>
          <b-col>
            <b-row>
                <div class="align-items-center">
                  <b-avatar
                    variant="info"
                    :src="require('../images/Developer.png')"
                    size="400"
                    to="/developerlogin">
                  </b-avatar>
                </div>
            </b-row>
            <b-row>
                <div class="align-items-center">
                  <b-button
                    pill class="v-btn"
                    to="/registerdev">
                    Get Started
                  </b-button>
                </div>
            </b-row>
          </b-col>
          <b-col>
            <b-row>
              <div class="align-items-center">
                  <b-avatar
                    variant="info"
                    :src="require('../images/Company.png')"
                    size="400"
                    to="/companylogin">
                  </b-avatar>
              </div>
            </b-row>
            <b-row>
              <div class="align-items-center">
                <b-button
                  pill class="v-btn"
                  to="/registercom">
                  Get Started
                </b-button>
              </div>
            </b-row>
          </b-col>
        </b-row>
         <b-row style="margin-top: 10vh">
           <strong>WAMJACK INCORPORATED, STELLENBOSCH WESTERN CAPE</strong><br>
           <strong>WAMJACK CONNECT AND ALL OTHER WAMJACK PRODUCTS ARE
             TRADEMARKS OF WAMJACK PROPERTIES, INC. © 2022</strong><br>
           <strong>ALL RIGHTS RESERVED. ALL OTHER TRADEMARKS AND TRADE
             NAMES ARE PROPERTIES OF THEIR RESPECTIVE OWNERS INCLUDING
           BUT NOT LIMITED TO MR DATABASE.</strong><br>
           <strong>WAMJACK - SOCIALLY DISTANCED NETWORKING SINCE 2020</strong>
         </b-row>
      </b-container>

      </div>
</template>

<script>
// @ is an alias to /src

export default {
  name: 'HomeView',
  components: {
  },
};
</script>

<style scoped>
#background{
  height: 100vh;
  min-height: 100vh;
}

h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}

.mint{
   background: #ff0000;
}

.cream{
   background: #eedecf;
}

.v-btn {
  width: 270px;
  height: 50px;
  color: #FFFFFF;
  background-color: #30106B;
  font-size: xx-large;
  text-align: center;
  margin-top: 15px;
}

p {
  margin: 0;
  padding: 0;
}

</style>
