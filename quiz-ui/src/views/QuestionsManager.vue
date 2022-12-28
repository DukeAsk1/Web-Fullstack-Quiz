<template>
  <div class="questions-manager">
    <h1>Questions Manager</h1>
    <h1>Question {{ currentQuestionPosition }} / {{ totalNumberOfQuestion }}</h1>
    <h1>{{ currentQuestion.questionTitle }}</h1>
    <h1>{{ currentQuestion.questionText }}</h1>
    <div>
      Answer Selected : {{ selected.text }}
      Scores : {{ score }}

    </div>



    <div v-for="value in currentQuestion.possibleAnswers" :key="value">
      <input type="radio" v-model="selected" :value="value" /> {{ value.text }}
    </div>
    <!-- <QuestionDisplay :question="currentQuestion" @click-on-answer="answerClickedHandler" /> -->
  </div>

  <button @click="next_question">Next</button>




</template>

<script>
import QuestionDisplay from './QuestionDisplay.vue';
import quizApiService from "@/services/QuizApiService";
// console.log(selected);
export default {
  name: "Questions Manager",
  data() {
    return {
      currentQuestion: {
        questionTitle: "...",
        questionText: "...",
        possibleAnswers: {
          text: "...",
          isCorrect: 0
        }
      },
      selected: '',
      currentQuestionPosition: 1,
      totalNumberOfQuestion: 0,
      score: 0,
      answer_current_question: {
        index: 0,
        answer: "...",
        correct: '...',
      },
      list_of_answers: [],
    };
  },
  components: {
    QuestionDisplay
  },
  async created() {
    let currentQuestion = await this.loadQuestionByposition();
    this.currentQuestion.questionTitle = currentQuestion.data.title;
    this.currentQuestion.questionText = currentQuestion.data.text;
    this.currentQuestion.possibleAnswers = currentQuestion.data.possibleAnswers;

    let nb_question = await this.getNumberOfQuestion();
    this.totalNumberOfQuestion = nb_question.data.nb_question;
    // this.value = this.value;
    // console.log(this.selected.isCorrect);
    //this.score = this.calculateScore(value);
    await this.getCorrectAnswer();



  },
  methods: {
    loadQuestionByposition() {
      return quizApiService.getQuestion(this.currentQuestionPosition)
    },
    getCorrectAnswer() {
      for (let i = 0; i <= this.currentQuestion.possibleAnswers.length - 1; i++) {
        if (this.currentQuestion.possibleAnswers[i].isCorrect === true) {
          this.answer_current_question.correct = this.currentQuestion.possibleAnswers[i].text;
        }
      }
      // for (value in this.currentQuestion.possibleAnswers) {

      // }
      console.log(this.answer_current_question.correct);
    },
    getNumberOfQuestion() {
      return quizApiService.getNumberOfQuestion()
    },
    calculateScore() {
      // for (const element of this.currentQuestion) {
      //   console.log(element);
      //   if (element.isCorrect === true) {
      //     console.log(element)
      //     this.answer_current_question.correct = this.element.text;
      //   }
      // }
      if (this.selected.isCorrect === true) {
        this.score = 1;
      }
      else {
        this.score = 0;
      }
    },
    next_question() {
      this.answer_current_question.index = this.currentQuestionPosition;
      this.answer_current_question.answer = this.selected.text;
      this.getCorrectAnswer();
      this.list_of_answers.push(this.answer_current_question);

      console.log(this.list_of_answers);
    },
    answerClickedHandler() {
    },
    endQuiz() {
    },
  },
  watch: {
    // watch for changes to the selected property
    selected: {
      handler() {
        try {
          for (answer in this.currentQuestion.possibleAnswers) {
            console.log(answer);
          }
        }
        catch (e) { }
        // console.log(this.currentQuestion.possibleAnswers);

        this.calculateScore()
      },
      immediate: true,
    },
  },
  /*computed: {
    totalNumberOfQuestion: function () {
      console.log(Object.values(this.getNumberOfQuestion()))
      return Object.values(this.getNumberOfQuestion())
    }
  }*/
};
</script>