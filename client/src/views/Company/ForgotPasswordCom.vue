<template>
<!-- The background colour is assigned from their respective views (dev/comp) -->
  <div :style="{ backgroundImage: 'url(' + require('../../assets/HomeBackground.png') + ')',
              backgroundPosition: 'center center',
              backgroundSize: '',
              }" id="background">
    <b-container fluid>
        <!-- The page uses a one row and five columns to properly space the elements -->
        <b-row class = dev_row>
          <b-col></b-col>
          <b-col id="card-col" cols="4" style="min-width: 40vw" >
              <div class="card">
                <b-card-img :src="require('../../assets/ConnectLogo.png')"></b-card-img>
                <p class = heading >
                  Forgot Your Password ?
                </p>
                <strong style="margin-bottom: 2vh">
                  In order to start the recovery process,
                  please enter your accounts email address:
                </strong>
                <b-form-input
                v-model="email"
                placeholder="Account Email Address"
                class = text-center
                ></b-form-input>
                <b-button @click="sendEmail()" style="margin-bottom: 4vh" variant="primary">
                  Send Me An Email
                </b-button>
                <br>
                <strong style="margin-bottom: 2vh">
                  The email sent to you will contain a verification code.<br/>
                  Copy and paste the verification here:
                </strong>
                <b-form-input
                v-model="code"
                placeholder="Verification Code"
                class = text-center
                style="margin-bottom: 4vh"
                ></b-form-input>
                <strong style="margin-bottom: 2vh">
                  Enter your new password here:
                </strong >
                <b-form-input
                v-model="pass1"
                placeholder="New Password"
                type="password"
                class = text-center
                style="margin-bottom: 4vh"
                ></b-form-input>
                <strong style="margin-bottom: 2vh">
                  Confirm your new password:
                </strong>
                <b-form-input
                v-model="pass2"
                placeholder="Confirm Password"
                class = text-center
                type="password"
                style="margin-bottom: 2vh"
                ></b-form-input>
                <b-button variant="primary" style="margin-bottom: 2vh"
                @click="verifyCode()">Verify and Update Password</b-button>
                <b-button variant="primary" style="margin-bottom: 2vh"
                to="/">Return to Home</b-button>
              </div>
          </b-col>
          <b-col></b-col>
        </b-row>
    </b-container>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'forgotPasswordCom',
  data() {
    return {
      email: '',
      hash: '',
      code: '',
      pass1: '',
      pass2: '',
    };
  },
  methods: {
    async sendEmail() {
      await axios.post('http://127.0.0.1:5000/forgotpasswordCom', {
        email: this.email,
      }).then((response) => {
        // eslint-disable-next-line prefer-destructuring
        this.hash = response.data[0];
        alert('An email has been sent to the email address specified. Follow the instructions.');
        console.log(response);
      }).catch((err) => {
        alert('Error. Your email address is not linked to a current user.');
        console.log(err);
      });
    },
    async verifyCode() {
      if (this.code.localeCompare(this.hash) !== 0) {
        alert('The verification code is incorrect.');
      } else if (this.pass1.localeCompare(this.pass2) !== 0) {
        alert('Your passwords did not match. Please check your spelling.');
      } else {
        await axios.put('http://127.0.0.1:5000/forgotpasswordCom', {
          email: this.email,
          newPass: this.pass1,
        }).then((response) => {
          alert('SUCCESSFUL. Your password has been updated.');
          console.log(response);
        }).catch((err) => {
          alert('Unexpected Error');
          console.log(err);
        });
      }
    },
  },
};
</script>

<style scoped>
#card-col {
  display: flex;
  justify-content: center;
}
.dev_row {
  display: flex;
  min-height: 100vh;
  align-items: center;
  align-content: center;
}
.heading {
  font-size: 5vh;
  color: #0D6EFDFF;
}

</style>
