<template>
  <div class="container" style="margin-top: 8rem">
    <div class="row gy-5">
      <div class="col-12 text-center">
        <h1>HomePage</h1>
      </div>

      <!-- Leaderboard -->
      <div class="col-12">
        <RankingsVue />
      </div>
      <!--  -->

      <div class="col-12 text-center">
        <button class="btn btn-success">
          <!-- hover effect to fix -->
          <router-link class="text-light" to="/new-quiz-page"
            >Let's start !</router-link
          >
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
