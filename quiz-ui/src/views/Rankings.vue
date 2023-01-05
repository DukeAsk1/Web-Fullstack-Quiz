<template>
  <div class="container-fluid">
    <div class="row">
      <div
        class="col-lg-6 offset-lg-3 justify-content-center align-items-center"
      >
        <table class="table table-striped text-light">
          <caption class="caption-top text-light">
            <h4>Scores précédents</h4>
          </caption>
          <thead>
            <tr>
              <th>Pseudo</th>
              <th>Score</th>
              <th>Date</th>
            </tr>
          </thead>
          <tr
            v-for="scoreEntry in registeredScores.scores"
            v-bind:key="scoreEntry.date"
          >
            <th>{{ scoreEntry.playerName }}</th>
            <th>{{ scoreEntry.score }}</th>
            <th>{{ scoreEntry.date }}</th>
          </tr>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import quizApiService from "@/services/QuizApiService";

export default {
  name: "Rankings",
  data() {
    return {
      registeredScores: [],
      playerName: "",
    };
  },

  props: {
    currentPlayer: {
      type: Object,
    },
  },

  async created() {
    let quizInfo = await quizApiService.getQuizInfo();
    this.registeredScores = quizInfo.data;
  },
};
</script>
