<template>
  <ul>
    Page for question Modifier
  </ul>
  <form>
    <div class="col">
      <label>Title</label>
      <input type="text" placeholder="Title" v-model="question.title">
    </div>

    <div class="col">
      <label>Text</label>
      <input type="text" placeholder="Text" v-model="question.text">
    </div>

    <div class="col">
      <label>Image</label>
      <input type="image" placeholder="Image" v-model="question.image">
    </div>

    <div class="col">
      <label>Answers</label>
      <div class='col'>
        <div>
          <label>Answer N°1</label>
          <div class="col">
            <label>Text</label>
            <input v-model="answer_1.text">
          </div>
          <div class="col">
            <label>Correct</label>
            <select class="form-select" v-model="answer_1.isCorrect">
              <option selected value=false>False</option>
              <option value=true>True</option>
            </select>
          </div>
        </div>
      </div>
      <div class='col'>
        <div>
          <label>Answer N°2</label>
          <div class="col">
            <label>Text</label>
            <input v-model="answer_2.text">
          </div>
          <div class="col">
            <label>Correct</label>
            <select class="form-select" v-model="answer_2.isCorrect">
              <option selected value=false>False</option>
              <option value=true>True</option>
            </select>
          </div>
        </div>
      </div>
      <div class='col'>
        <div>
          <label>Answer N°3</label>
          <div class="col">
            <label>Text</label>
            <input v-model="answer_3.text">
          </div>
          <div class="col">
            <label>Correct</label>
            <select class="form-select" v-model="answer_3.isCorrect">
              <option selected value=false>False</option>
              <option value=true>True</option>
            </select>
          </div>
        </div>
      </div>
      <div class='col'>
        <div>
          <label>Answer N°4</label>
          <div class="col">
            <label>Text</label>
            <input v-model="answer_4.text">
          </div>
          <div class="col">
            <label>Correct</label>
            <select class="form-select" v-model="answer_4.isCorrect">
              <option selected value=false>False</option>
              <option value=true>True</option>
            </select>
          </div>
        </div>
      </div>
    </div>
  </form>
</template>

<script>
export default {
  name: "QuestionModifier",
  props: {
    question: {
      type: Object
    },
    emits: ["update:question"]
  },
  data() {
    return {
      answer_1: {
        text: null,
        isCorrect: null
      },
      answer_2: {
        text: null,
        isCorrect: null
      },
      answer_3: {
        text: null,
        isCorrect: null
      },
      answer_4: {
        text: null,
        isCorrect: null
      },
    }
  },
  mounted() {
    // Destructure the first element from the names prop
    if (this.question.possibleAnswers) {
      const [answer_1, answer_2, answer_3, answer_4] = this.question.possibleAnswers;
      this.answer_1 = answer_1 ? answer_1 : { text: null, isCorrect: null }
      this.answer_2 = answer_2 ? answer_2 : { text: null, isCorrect: null }
      this.answer_3 = answer_3 ? answer_3 : { text: null, isCorrect: null }
      this.answer_4 = answer_4 ? answer_4 : { text: null, isCorrect: null }
    }

  }
}
</script>