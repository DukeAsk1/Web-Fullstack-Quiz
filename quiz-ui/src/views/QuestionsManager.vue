<template>
  <div class="questions-manager">
    <h1>Questions Manager</h1>
    <h1>Question {{ currentQuestionPosition }} / {{ totalNumberOfQuestion }}</h1>

    <QuestionDisplay :question="currentQuestion" @click-on-answer="answerClickedHandler" />
  </div>

  <button v-if="currentQuestionPosition != totalNumberOfQuestion" @click="next_question">Next</button>





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
  mounted() {
    // const answer_list = sessionStorage.getItem('list_of_answers');
    // const ongoing_score = sessionStorage.getItem('score');
    // const position = sessionStorage.getItem('position');

    // console.log(answer_list);

    // this.list_of_answers = answer_list;
    // this.score = ongoing_score;
    // this.currentQuestionPosition = position;

    //   try {
    //     // Something that throws exception
    //     const answer_list = sessionStorage.getItem('list_of_answers');
    //     this.list_of_answers = answer_list;
    //   }
    //   catch (e) {
    //     this.list_of_answers = [];
    //   }
    try {
      // Something that throws exception
      const ongoing_score = sessionStorage.getItem('score');
      this.score = ongoing_score;
      console.log(this.score);
    }
    catch (e) {
      this.score = 0;
    }
    //   try {
    //     // Something that throws exception
    //     const position = sessionStorage.getItem('position');
    //     this.currentQuestionPosition = position;
    //   }
    //   catch (e) {
    //     this.currentQuestionPosition = 1;
    //   }
  },
  async created() {
    this.currentQuestion = await this.loadQuestionByposition(this.currentQuestionPosition);
    // this.currentQuestion.questionTitle = currentQuestion.data.title;
    // this.currentQuestion.questionText = currentQuestion.data.text;
    // this.currentQuestion.possibleAnswers = currentQuestion.data.possibleAnswers;

    let nb_question = await this.getNumberOfQuestion();
    this.totalNumberOfQuestion = nb_question.data.nb_question;
    // this.value = this.value;
    // console.log(this.selected.isCorrect);
    //this.score = this.calculateScore(value);
    //await this.getCorrectAnswer();
  },
  methods: {
    async loadQuestionByposition(currentQuestionPosition) {
      let current_question = quizApiService.getQuestion(currentQuestionPosition);
      let data = await current_question.data;
      return data
    },
    getCorrectAnswer() {
      for (let i = 0; i <= this.currentQuestion.possibleAnswers.length - 1; i++) {
        if (this.currentQuestion.possibleAnswers[i].isCorrect === true) {
          this.answer_current_question.correct = this.currentQuestion.possibleAnswers[i].text;
        }
      }
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
        this.score++;
      }
      else {
        this.score;
      }
    },
    next_question() {
      const selectedAnswer = this.selected;
      // const answer = this.currentQuestion.flatMap(currentQuestion => 
      //                                     currentQuestion.possibleAnswers).find(possibleAnswers => 
      //                                     possibleAnswers.id === selectedAnswer);
      if (selectedAnswer.isCorrect) {
        this.score++;
      }

      this.answer_current_question.index = this.currentQuestionPosition;
      this.answer_current_question.answer = this.selected.text;
      this.getCorrectAnswer();
      this.list_of_answers.push(this.answer_current_question);
      this.currentQuestionPosition++;
      //this.calculateScore();
      console.log('new position');
      console.log(this.currentQuestionPosition);
      this.currentQuestion = this.loadQuestionByposition(this.currentQuestionPosition);
      console.log(this.currentQuestion);

      this.currentQuestion.questionTitle = currentQuestion.data.title;
      this.currentQuestion.questionText = currentQuestion.data.text;
      this.currentQuestion.possibleAnswers = currentQuestion.data.possibleAnswers;
      // sessionStorage.setItem('list_of_answers', this.list_of_answers);
      // sessionStorage.setItem('score', this.score);
      // sessionStorage.setItem('position', this.currentQuestionPosition);
      // console.log(this.list_of_answers);
      // console.log(this.answer_current_question);
      // console.log(sessionStorage);

      // location.reload();
    },
    answerClickedHandler() {
    },
    endQuiz() {
    },
  },
  // watch: {
  //   // watch for changes to the selected property
  //   selected: {
  //     handler() {
  //       console.log(this.list_of_answers)
  //       try {
  //         for (answer in this.currentQuestion.possibleAnswers) {
  //           console.log(answer);
  //         }
  //       }
  //       catch (e) { }
  //       // console.log(this.currentQuestion.possibleAnswers);

  //       this.calculateScore();
  //     },
  //     immediate: true,
  //   },
  // },
  /*computed: {
    totalNumberOfQuestion: function () {
      console.log(Object.values(this.getNumberOfQuestion()))
      return Object.values(this.getNumberOfQuestion())
    }
  }*/
};
</script>