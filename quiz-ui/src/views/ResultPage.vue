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
          Detail of your attempt :
          <ul v-for="answer in list_of_result.answers_list" :key="answer">
            <h2>Question : {{ answer[0] }}</h2>
            <a>
              Your answer : {{ answer[1] }}
            </a>
            <a>
              The correct answer : {{ answer[3] }}
            </a>
          </ul>
        </a>
      </li>
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
</style>


<script>

/*

pour les résultats, afficher la question, la réponse selectionnée, la bonne réponse,
et une image en fonction du résultat, flèche verte si égale, flèche rouge si non



*/







import QuestionDisplay from './QuestionDisplay.vue';
import quizApiService from "@/services/QuizApiService";
// console.log(selected);
export default {
  name: "Questions Manager",
  data() {
    return {
      leaderboard: {
        username: "...",
        score: 0
      },
      score: 0,
      answer_current_question: {
        index: 0,
        answer: "...",
        correct: '...',
      },
      list_of_result: Array(),
    };
  },
  components: {
    QuestionDisplay
  },

  async created() {

    // parse the list as JSON
    this.list_of_result = JSON.parse(window.localStorage.getItem('result_quiz')).data;
    console.log("Result page quiz", this.list_of_result);
    console.log(this.list_of_result.playerName)

  },

};
</script>