<template>
  <div class="question-display">
    <h1>Question Display</h1>
    <img v-if="question.image" :src="test.jpg" /> <a @click="$emit('answer-selected', 2)">La réponse D</a>
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
    created() {
      this.$emit('answer-selected', 2);
    },
  }
};
</script>