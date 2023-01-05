<template>
  <div class="container-fluid">
    <div class="row">
      <div class="col-lg-6 offset-lg-3 justify-content-center align-items-center">
        <table class="table table-striped">
          <caption class="caption-top">
            <h4>Scores précédents</h4>
          </caption>
          <thead>
            <tr>
              <th>Pseudo</th>
              <th>Score</th>
              <th>Date</th>
            </tr>
          </thead>
          <div class="row" v-if="action === 'start'">
            <tr v-for="scoreEntry in registeredScores.scores" v-bind:key="scoreEntry.date">
              <th>{{ scoreEntry.playerName }}</th>
              <th>{{ scoreEntry.score }}</th>
              <th>{{ scoreEntry.date }}</th>
            </tr>
          </div>
          <div class="row" v-if="action === 'end'" v-try="getEndResult()">
            <tr v-for="scoreEntry in registeredScores.scores" v-bind:key="scoreEntry.date">
              <th>{{ scoreEntry.playerName }}</th>
              <th>{{ scoreEntry.score }}</th>
              <th>{{ scoreEntry.date }}</th>
            </tr>
          </div>
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
      list_of_result: Array(),
    };
  },
  computed: {

  },
  props: {
    currentPlayer: {
      type: Object,
    },
    action: "",
  },

  async created() {

    let quizInfo = await quizApiService.getQuizInfo();
    this.registeredScores = quizInfo.data;
  },
};
</script>
