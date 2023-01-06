<template>
  <div class="container" style="height: 20vh">
    <div class="row">
      <div class="col-lg-6 offset-lg-3 justify-content-center align-items-center">
        <table class="table table-striped">
          <caption class="caption-top">
            <h4 align="center">Previous Scores</h4>

          </caption>
          <thead>
            <tr align="center">
              <th>Pseudo</th>
              <th>Score</th>
              <th>Date</th>
            </tr>
          </thead>
          <tr v-if="table === 'start'" v-for="scoreEntry in registeredScores.scores" v-bind:key="scoreEntry.date"
            align="center">
            <th>{{ scoreEntry.playerName }}</th>
            <th>{{ scoreEntry.score }}</th>
            <th>{{ scoreEntry.date }}</th>
          </tr>

          <tr v-if="table === 'end'" v-for="scoreEntry in registeredScores.scores" v-bind:key="scoreEntry.date"
            :class="getEndResult()" align="center">
            <!-- :class="highlight_current_score(scoreEntry)"> -->
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
  props: {
    currentPlayer: {
      type: Object,
    },
    table: "",
  },
  data() {
    return {
      registeredScores: [],
      playerName: "",
      list_of_result: Array(),
    };
  },

  computed: {
    highlight_current_score(value) {
      if (
        value.date === this.list_of_result.date_attempt &&
        value.playerName === this.list_of_result.playerName &&
        value.score === this.list_of_result.score
      ) {
        return value === value ? "success" : "";
      }
    },
  },


  async created() {

    let quizInfo = await quizApiService.getQuizInfo();
    this.registeredScores = quizInfo.data;
    // console.log("log RANKING", this.action);
  },
  methods: {
    async getEndResult() {
      this.list_of_result = JSON.parse(
        window.localStorage.getItem("result_quiz")
      ).data;
      return this.list_of_result;
    },
    async highlight_current_score(value) {
      if (
        value.date === this.list_of_result.date_attempt &&
        value.playerName === this.list_of_result.playerName &&
        value.score === this.list_of_result.score
      ) {
        return value === value ? "highlight" : "";
      }
    },
  }
};
</script>

<style>
.success {
  background-color: green;
}
</style>
