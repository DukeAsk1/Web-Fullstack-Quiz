<template>
  <div class="container text-center">
    <div class="row gy-3">
      <div v-if="action === 'newQuestion'">
        <div class="row">
          <label for="name-input">Import a question from a JSON file :</label>
        </div>
        <input type="file" accept=".json" v-on:change="import_json" />
      </div>
    </div>

    <form>
      <div class="card w-50 offset-3 p-4 rounded-4">
        <!-- Position Titre Question Image -->
        <div class="container">
          <div class="row">
            <div class="col-6 offset-3">
              <h3>Position</h3>
              <input
                type="text"
                placeholder="Title"
                v-model="question.position"
              />
            </div>
          </div>
          <div class="row mt-2">
            <div class="row">
              <div class="col-6 offset-3">
                <div class="row">
                  <div class="col">
                    <label>Title</label>
                    <input
                      type="text"
                      placeholder="Title"
                      v-model="question.title"
                    />
                  </div>

                  <div class="col">
                    <label>Question</label>
                    <input
                      type="text"
                      placeholder="Text"
                      v-model="question.text"
                    />
                  </div>
                </div>
              </div>
            </div>

            <div class="col-12 mt-4">
              <p>Image</p>
              <img :src="question.image" ref="image" @change="convertToImage" />
              <input
                type="file"
                placeholder="Image"
                accept="image/*"
                @change="convertToBase64"
              />
            </div>
          </div>
        </div>

        <!--  -->

        <!-- Answers -->
        <div>
          <label v-if="too_many">TOO MANY ANSWERS IN CHOICES</label>
        </div>

        <div class="row mt-5">
          <h3>Answers</h3>
          <div class="col">
            <div>
              <div class="col">
                <label>Answer N°1</label>
                <input v-model="answer_1.text" />
              </div>
              <div class="col-8 offset-2">
                <div class="row">
                  <div class="col-4">
                    <label>Correct</label>
                  </div>
                  <div class="col">
                    <select class="form-select" v-model="answer_1.isCorrect">
                      <option selected value="0">False</option>
                      <option value="1">True</option>
                    </select>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="col">
            <div>
              <div class="col">
                <label>Answer N°2</label>
                <input v-model="answer_2.text" />
              </div>
              <div class="col-8 offset-2">
                <div class="row">
                  <div class="col-4">
                    <label>Correct</label>
                  </div>
                  <div class="col">
                    <select class="form-select" v-model="answer_2.isCorrect">
                      <option selected value="0">False</option>
                      <option value="1">True</option>
                    </select>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="col">
            <div>
              <div class="col">
                <label>Answer N°3</label>
                <input v-model="answer_3.text" />
              </div>
              <div class="col-8 offset-2">
                <div class="row">
                  <div class="col-4">
                    <label>Correct</label>
                  </div>
                  <div class="col">
                    <select class="form-select" v-model="answer_3.isCorrect">
                      <option selected value="0">False</option>
                      <option value="1">True</option>
                    </select>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="col">
            <div>
              <div class="col">
                <label>Answer N°4</label>
                <input v-model="answer_4.text" />
              </div>
              <div class="col-8 offset-2">
                <div class="row">
                  <div class="col-4">
                    <label>Correct</label>
                  </div>
                  <div class="col">
                    <select class="form-select" v-model="answer_4.isCorrect">
                      <option selected value="0">False</option>
                      <option value="1">True</option>
                    </select>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <!--  -->
      </div>
    </form>
  </div>
  <div class="row mt-3">
    <div class="col-2 offset-5">
      <div class="row">
        <div class="col-3 offset-3">
          <button class="btn btn-success" style="width: 5rem" @click="save">
            Save
          </button>
        </div>

        <div class="col">
          <button
            class="btn btn-danger"
            style="width: 5rem"
            @click="sendToPreviousPage()"
          >
            Back
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "QuestionModifier",
  props: {
    question: {
      type: Object,
    },
    action: "",
    emits: ["update:question"],
  },
  data() {
    console.log("in modifier windows");
    return {
      answer_1: {
        text: null,
        isCorrect: null,
      },
      answer_2: {
        text: null,
        isCorrect: null,
      },
      answer_3: {
        text: null,
        isCorrect: null,
      },
      answer_4: {
        text: null,
        isCorrect: null,
      },
      base64Image: "",
      updatedAnswersArray: Array(),
      too_many: "",
    };
  },

  mounted() {
    // Destructure the first element from the names prop
    if (this.question.possibleAnswers) {
      const [answer_1, answer_2, answer_3, answer_4] =
        this.question.possibleAnswers;
      this.answer_1 = answer_1 ? answer_1 : { text: null, isCorrect: null };
      this.answer_2 = answer_2 ? answer_2 : { text: null, isCorrect: null };
      this.answer_3 = answer_3 ? answer_3 : { text: null, isCorrect: null };
      this.answer_4 = answer_4 ? answer_4 : { text: null, isCorrect: null };
    }
  },
  methods: {
    convertToBase64(event) {
      // Reference to the DOM input element
      const input = event.target;
      // Ensure that you have a file before attempting to read it
      if (input.files && input.files[0]) {
        // create a new FileReader to read this image and convert to base64 format
        const reader = new FileReader();
        // Define a callback function to run, when FileReader finishes its job
        reader.onload = (e) => {
          // Note: arrow function used here, so that "this.base64Image" refers to the image data in Vue component
          // Read image as base64 and set to base64Image
          this.base64Image = e.target.result;
          this.question.image = this.base64Image;
        };
        // Start the reader job - read file as a data url (base64 format)
        reader.readAsDataURL(input.files[0]);
      }
    },
    save() {
      if (this.answer_1.text) {
        this.updatedAnswersArray.push({
          text: this.answer_1.text,
          isCorrect: this.answer_1.isCorrect,
        });
      }
      if (this.answer_2.text) {
        this.updatedAnswersArray.push({
          text: this.answer_2.text,
          isCorrect: this.answer_2.isCorrect,
        });
      }
      if (this.answer_3.text) {
        this.updatedAnswersArray.push({
          text: this.answer_3.text,
          isCorrect: this.answer_3.isCorrect,
        });
      }
      if (this.answer_4.text) {
        this.updatedAnswersArray.push({
          text: this.answer_4.text,
          isCorrect: this.answer_4.isCorrect,
        });
      }
      this.$emit("update:question", {
        position: this.question.position,
        title: this.question.title,
        text: this.question.text,
        image: this.question.image,
        possibleAnswers: this.updatedAnswersArray,
      });
      console.log("base 64", this.base64Image);
      console.log("POSSIBLE ANSWERSSSSS", this.updatedAnswersArray);
    },
    import_json(event) {
      const file = event.target.files[0];

      if (!file) {
        return;
      }

      const reader = new FileReader();
      reader.onload = (e) => {
        const json = JSON.parse(e.target.result);
        // Do something with the JSON data here
        this.question.position = json.position;
        this.question.image = json.image;
        this.question.text = json.text;
        this.question.title = json.title;
        this.question.possibleAnswers = json.possibleAnswers;

        // console.log(this.question.possibleAnswers)
        if (this.question.possibleAnswers.length > 4) {
          this.too_many = "too many input answers";
        }

        for (let i = 0; i < this.question.possibleAnswers.length; i++) {
          console.log("index i in answers", this.question.possibleAnswers[i]);
          if (this.question.possibleAnswers[i].isCorrect === true) {
            this.question.possibleAnswers[i].isCorrect = 1;
          } else if (this.question.possibleAnswers[i].isCorrect === false) {
            this.question.possibleAnswers[i].isCorrect = 0;
          }
        }
        const [answer_1, answer_2, answer_3, answer_4] =
          this.question.possibleAnswers;
        this.answer_1 = answer_1;
        this.answer_2 = answer_2;
        this.answer_3 = answer_3;
        this.answer_4 = answer_4;
        // this.updatedAnswersArray.push(answer_1);
        // this.updatedAnswersArray.push(answer_2);
        // this.updatedAnswersArray.push(answer_3);
        // this.updatedAnswersArray.push(answer_4);

        // {
        // "id": 1,
        // "position": 1,
        // "text": "What team won the NBA Championship in 2020?",
        // "title": "NBA",
        // "possibleAnswers": [
        // {"text": "Los Angeles Lakers", "isCorrect": true},
        // {"text": "Golden State Warriors", "isCorrect": false},
        // {"text": "Boston Celtics", "isCorrect": false},
        // {"text": "Houston Rockets", "isCorrect": false}
        // ]
        // }
      };
      reader.readAsText(file);
    },
    sendToPreviousPage() {
      this.$router.go(-1);
    },
  },
};
</script>
