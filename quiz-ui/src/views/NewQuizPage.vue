<template>
  <div class="container" style="margin-top: 10rem">
    <div class="row g-3">
      <div class="col-4 offset-4 text-center">
        <h1>New quiz !</h1>
      </div>

      <div class="col-4 offset-4 text-center">
        <p>Please enter your username</p>
      </div>

      <div class="col-4 offset-4">
        <!-- todo inputfloat -->
        <div class="form-floating mb-3">

          <input type="text" class="form-control" v-model="username" id="name" name="name" placeholder="votrepseudo" />
          <label class="text-dark" for="name">Username</label>
        </div>
      </div>

      <div class="col-4 offset-4 text-center mt-3">

        <button class="btn btn-success" @click="launchNewQuiz">GO !</button>
      </div>

      <div class="col-6 offset-3 text-center alert alert-danger alert-dismissible fade show" role="alert"
        v-if="!username && wrongSubmit">
        <strong>Error !</strong> Please enter a username in the above field
      </div>
    </div>
  </div>
</template>

<script>
import participationStorageService from "@/services/ParticipationStorageService";
export default {
  name: "HomePage",
  data() {
    return {
      username: "",
      wrongSubmit: false,
    };
  },
  methods: {
    buttonClickHandler() {
      console.log("Compute playerName");
      this.username = this.data.username;
    },
    launchNewQuiz() {
      //Si le pseudo n'est pas renseigné
      if (this.username.toString() === "") {
        this.wrongSubmit = true;
        return;
      }
      participationStorageService.savePlayerName(this.username.toString());
      const playerName = participationStorageService.getPlayerName();
      console.log("Launch new quiz with " + playerName);
      this.$router.push("/questions-manager");
    },
  },
};
</script>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: all .5s;
}

.fade-enter,
.fade-leave-to {
  opacity: 0;
}
</style>
