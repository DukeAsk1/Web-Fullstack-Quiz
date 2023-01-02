<template>
  <ul>
    <li v-for="question in list_of_question">
      {{ question.position }} /
      {{ question.text }}
      {{ question.possibleAnswers }}
      <a @click="$emit('modify', question.position)">
        Modify
      </a>
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
    emits: ["modify"]
  }
};
</script>