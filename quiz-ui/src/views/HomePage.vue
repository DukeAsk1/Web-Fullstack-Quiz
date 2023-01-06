<template>
  <div class="container" style="margin-top: 8rem">
    <div class="row gy-5">
      <div class="col-12 text-center">
        <h1>HomePage</h1>
  <div class="container" style="margin-top: 8rem">
    <div class="row gy-5">
      <div class="col-12 text-center">
        <h1>HomePage</h1>
      </div>

      <!-- Leaderboard -->
<<<<<<< HEAD
      <div align="center">
        <h2>The leaderboard for the quiz:</h2>
        <RankingsVue :table="table" />
      </div>
=======

      <div class="col-12">
        <RankingsVue :table="table" />
      </div>

>>>>>>> 5b8306535b2e4929a3a7f1fccd3dc5dfb3e34369
      <!--  -->

      <div class="col-12 text-center">
      <div class="col-12 text-center">
        <button class="btn btn-success">
          <!-- hover effect to fix -->


          <transition name="fade">
            <router-link class="text-light" to="/new-quiz-page">Let's start !</router-link>
            <router-link class="text-light" to="/new-quiz-page">Let's start !</router-link>
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
      table: "start",
    };
  },

  components: {
    RankingsVue,
  },

  async created() {
    console.log("Composant Home page 'created'");

    let quizInfo = await quizApiService.getQuizInfo();
    this.registeredScores = quizInfo.data;
    console.log(this.table);
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
