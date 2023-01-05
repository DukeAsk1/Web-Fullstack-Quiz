<template>
  <ul>

    <div class="row">
      <!-- Left -->
      <div class="col-6">
        <div class="col-fluid">
          <h3>Voici tes réponses :</h3>
        </div>

        <div class="col">
          <div class="row gy-4">
            <div class="col-fluid" v-for="question in list_of_question" :key="question">
              <h4>Question : {{ question.text }}</h4>
              <p>
                <img :src="question.image" /> <br />
                Position : {{ question.position }} <br />
              <div class="col-fluid" v-for="answer in question.possibleAnswers" :key="answer">
                Answer : {{ answer.text }} Value : {{ answer.isCorrect }}
              </div>
              </p>
              <button @click="$emit('modify', question.position)" class="btn btn-warning">
                Modify
              </button>
              <button @click="$emit('delete', question.id)" class="btn btn-danger">
                Delete
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    <!-- <li v-for="question in list_of_question">
      {{ question.position }} /
      {{ question.text }}
      {{ question.possibleAnswers }} -->

    <!-- </li> -->
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
    emits: ["modify", "delete"]
  }
};
</script>