<template>
  <div class="about">
    <h1>This is the result page</h1>

    <div>
      <li>
        <a>
          Hi {{ list_of_result.playerName }}
        </a>
        <a>
          Your Score is : {{ list_of_result.score }}
        </a>

        <a>
          <label for='attempt_answers'>Detail of your attempt :</label>
          <!-- <select id="attempt_answers" size="100"> -->
          <ul v-for="answer in list_of_result.answers_list" :key="answer">
            <h2>Question : {{ answer[0] }}</h2>
            <a>
              Your answer : {{ answer[1] }}
            </a>
            <a>
              The correct answer : {{ answer[3] }}
            </a>
          </ul>
          <!-- </select> -->
        </a>
      </li>
    </div>
    <div>
      The leaderboard for the quiz:
      <table>
        <tr v-for="row in this.registeredScores.scores" :class="highlightClass(row)">
          <td>{{ row.playerName }}</td>
          <td>{{ row.score }}</td>
        </tr>
      </table>
    </div>
    <div>
      <button v-on:click="new_attempt">
        TRY AGAIN
      </button>
      <button v-on:click="home_page">
        HOME PAGE
      </button>


    </div>
  </div>
</template>

<style>
@media (min-width: 1024px) {
  .about {
    min-height: 100vh;
    display: flex;
    ;
  }
}

.highlight {
  background-color: yellow;
}
</style>


<script>

/*

pour les résultats, afficher la question, la réponse selectionnée, la bonne réponse,
et une image en fonction du résultat, flèche verte si égale, flèche rouge si non



*/

import QuestionDisplay from './QuestionDisplay.vue';
import quizApiService from "@/services/QuizApiService";
import participationStorageService from "@/services/ParticipationStorageService";
// console.log(selected);
export default {
  name: "Questions Manager",
  data() {
    return {
      registeredScores: [],
      score: 0,
      answer_current_question: {
        index: 0,
        answer: "...",
        correct: '...',
      },
      list_of_result: Array(),
    };
  },
  computed: {
    highlightClass(value) {
      if (value.date === this.list_of_result.date_attempt && value.playerName === this.list_of_result.playerName && value.score === this.list_of_result.score) {
        return value === value ? 'highlight' : '';
      }
    }
  },

  components: {
    QuestionDisplay
  },

  async created() {

    // parse the list as JSON
    this.list_of_result = JSON.parse(window.localStorage.getItem('result_quiz')).data;
    // console.log("Result page quiz", this.list_of_result);
    // console.log(this.list_of_result.playerName)
    let quizInfo = await quizApiService.getQuizInfo();
    this.registeredScores = quizInfo.data;
    console.log(this.registeredScores)
  },
  methods: {
    new_attempt() {
      this.$router.push('/questions-manager');
    },
    home_page() {
      participationStorageService.removePlayerName();
      this.$router.push('/');
    }
  }

};
</script>