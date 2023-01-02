<template>
  <h1>Home page</h1>
  <div>{{ registeredScores }}</div>

  <div v-for="scoreEntry in registeredScores" v-bind:key="scoreEntry.date">
    {{ scoreEntry.playerName }} - {{ scoreEntry.score }}
  </div>

  <router-link to="/start-new-quiz-page">Démarrer le quiz !</router-link>
</template>

<script>

import quizApiService from "@/services/QuizApiService";

export default {
  name: "HomePage",
  data() {
    return {
      registeredScores: [],
      playerName: ''
    };
  },

  async created() {
    console.log("Composant Home page 'created'");

    let quizInfo = await quizApiService.getQuizInfo();
    this.registeredScores = quizInfo.data;

  }
};
</script>

