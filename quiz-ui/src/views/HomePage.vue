<template>
  <div class="container">
    <div class="row">
      <div class="col text-center">
        <h1>Page d'accueil</h1>
      </div>

      <!-- Leaderboard -->
      <RankingsVue v-if="action === 'start'" />
      <!--  -->

      <div class="col text-center">
        <button class="btn btn-success">
          <!-- hover effect to fix -->
          <transition name="fade">
            <router-link class="text-light" to="/new-quiz-page">Démarrer le quiz !</router-link>
          </transition>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import quizApiService from "@/services/QuizApiService";
import RankingsVue from "./Rankings.vue";

export default {
  name: "HomePage",
  data() {
    return {
      registeredScores: [],
      playerName: "",
    };
  },

  components: {
    RankingsVue,
  },

  async created() {
    console.log("Composant Home page 'created'");

    let quizInfo = await quizApiService.getQuizInfo();
    this.registeredScores = quizInfo.data;
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
