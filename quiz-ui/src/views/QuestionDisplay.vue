<template>
  <div class="question-display">
    <h1>Question Display</h1>

    <h1>{{ question.title }}</h1>
    <h1>{{ question.text }}</h1>

    <img v-if="question.image" :src="question.image" />

    <div class="d-flex-column">
      <a v-for="(value, index) in question.possibleAnswers" @click="$emit('answer-selected', index)">
        <!-- :key="value"> -->
        <input type="radio" :value="value" name="radAnswer" />
        {{ value.text }}
      </a>
      <!-- <div>
        Answer Selected : {{ radAnswer }}
        Scores : {{ score }}
      </div> -->
    </div>

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