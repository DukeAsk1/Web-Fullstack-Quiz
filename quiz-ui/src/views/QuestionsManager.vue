<template>
  <div class="questions-manager">
    <h1>Questions Manager</h1>
    <h1>Question {{ currentQuestionPosition }} / {{ totalNumberOfQuestion }}</h1>
  <QuestionDisplay :question="currentQuestion" @click-on-answer="answerClickedHandler" />
  </div>
</template>

<script>
import QuestionDisplay from './QuestionDisplay.vue';
export default {
  name: "Questions Manager",
  data() {
    return {
      currentQuestion: {
        questionTitle: "...",
        questionText: "...",
        possibleAnswers: ["a", "b", "c", "d"]
      },
      currentQuestionPosition: 1,
    };
  },
  components: {
    QuestionDisplay
  },
  async created() {
    var loadQuestionByposition = loadQuestionByposition();
  },
  methods: {
    loadQuestionByposition() {
    },
    answerClickedHandler() {
    },
    endQuiz() {
    },

  }
};
</script>