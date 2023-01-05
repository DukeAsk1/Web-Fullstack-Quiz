<template>
  <div class="container">
    <div class="row g-3">
      <div class="col-4 offset-4 text-center">
        <h1>Nouveau quiz !</h1>
      </div>

      <div class="col-4 offset-4 text-center">
        <p>Veuillez saisir votre pseudonyme :</p>
      </div>

      <div class="col-4 offset-4">
        <!-- todo inputfloat -->
        <div class="form-floating mb-3">
          <input type="text" class="form-control" v-model="username" id="name" name="name" placeholder="votrepseudo" />
          <label class="text-dark" for="name">Pseudonyme</label>
        </div>
      </div>

      <div class="col-4 offset-4 text-center mt-3">
        <Transition name="fade">
          <RouterLink to="/questions-manager">
            <button class="btn btn-success" @click="launchNewQuiz">GO!</button>
          </RouterLink>
        </Transition>
      </div>

      <div class="col-6 offset-3 text-center alert alert-danger alert-dismissible fade show" role="alert"
        v-if="!username && wrongSubmit">
        <strong>Erreur !</strong> Veuillez entrer un pseudonyme dans le champ
        ci-dessus
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
      // this.$router.push("/questions-manager");
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
