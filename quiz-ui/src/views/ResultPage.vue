<template>
  <div class="about">
    <h1>This is the result page</h1>

    <ul v-for="item in list_of_answers" :key="item">
      <li>
        <a>
          {{ item.position }}
        </a>
        <a>
          {{ item.text }}
        </a>
      </li>
    </ul>
  </div>
</template>

<style>
@media (min-width: 1024px) {
  .about {
    min-height: 100vh;
    display: flex;
    align-items: center;
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
      list_of_answers: Array(),
    };
  },
  components: {
    QuestionDisplay
  },

  async created() {

    const list_of_answers = window.localStorage.getItem('list_of_answers');

    // parse the list as JSON
    this.list_of_answers = JSON.parse(list_of_answers);
    console.log(this.list_of_answers)
    // this.list_of_answers = window.localStorage.getItem("list_of_answers");
    // this.currentQuestion.questionTitle = currentQuestion.data.title;
    // this.currentQuestion.questionText = currentQuestion.data.text;
    // this.currentQuestion.possibleAnswers = currentQuestion.data.possibleAnswers;

  },

};
</script>