<template>
  <div class="question-display">
    <h1>Question Display</h1>

    <h1>{{ question.title }}</h1>
    <h1>{{ question.text }}</h1>

    <img v-if="question.image" :src="question.image" />
    <!-- <div>
      Answer Selected : {{ selected.text }}
      Scores : {{ score }}
    </div> -->

    <!-- <div v-for="value in currentQuestion.possibleAnswers" :key="value">
      <input type="radio" v-model="selected" :value="value" /> {{ value.text }}
    </div> -->
    <a v-for="(answer, index) in question.possibleAnswers" @click="$emit('answer-selected', index)">
      {{ answer.text }}
    </a>

  </div>
</template>


<script>
export default {
  name: "QuestionDisplay",
  props: {
    question: {
      type: Object
    },
    emits: ["answer-selected"],
    // created() {
    //   this.$emit('answer-selected', 2);
    // },
  }
};
</script>