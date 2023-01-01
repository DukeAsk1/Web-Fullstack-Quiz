<template>
  <ul>
    <li v-for="question in list_of_question">
      {{ question.text }}
      {{ question.possibleAnswers }}
      <span @click="$emit('question-edit', question.position)">
        Modify
      </span>
    </li>
  </ul>
</template>

<script>
export default {
  name: "QuestionList",
  data() {
    return {
      questions: Array()
    };
  },
  props: {
    list_of_question: {
      type: Object
    },
    emits: ["question-edit"]
  }
};
</script>