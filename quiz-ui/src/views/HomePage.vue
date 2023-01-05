<template>
  <div class="container">
    <div class="row">
      <div class="col text-center">
        <h1>Page d'accueil</h1>
      </div>
    </div>

    <button class="btn btn-success">
      <!-- hover effect to fix -->
      <router-link to="/admin">Admin Access</router-link>
    </button>

    <!-- Leaderboard -->
    <RankingsVue />
    <!--  -->

    <div class="col text-center">
      <button class="btn btn-success">
        <!-- hover effect to fix -->
        <router-link to="/new-quiz-page">Démarrer le quiz !</router-link>
      </button>
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
