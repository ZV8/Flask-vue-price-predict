<template>
  <div class="container" style="max-width: 1540px;">
    <div class="row">
      <div class="col-sm-12">
        <h1>Прогнозирование стоимости аренды жилья в Москве</h1>
        <h3>на основании собранных данных об объектах с cian.ru (весна 2021)</h3>
        <hr><br><br>
        <alert :message=message v-if="showMessage"></alert>
        <button type="button" class="btn btn-success" v-b-modal.example-modal>
          Сделать прогноз
        </button>
        <br><br>
        <table class="table table-hover">
          <thead>
            <tr style="color:#000;font-size:12px;">
              <th scope="col" width="100px">Дата прогноза</th>
              <th scope="col" width="100px">Кол-во комнат</th>
              <th scope="col" width="180px">Площадь: <br>общая / кухни / жилая</th>
              <th scope="col" width="100px">Этаж / <br>Этажность</th>
        <!--  <th scope="col">lat_lng_min</th>-->
              <th scope="col" width="150px">Метро</th>
              <th scope="col" width="200px">Время до метро</th>
              <th scope="col" width="350px">Описание</th>
              <th scope="col">Прогноз цены</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(example, index) in examples" :key="index">
              <td><span style="color:#999;font-size:12px;">{{ example.date }}</span></td>
              <td>{{ example.roomsCount }}</td>
              <td>
                {{ example.totalArea }} / {{ example.kitchenArea }} / {{ example.livingArea }}
              </td>
              <td>{{ example.floorNumber }} / {{ example.floorsCount }}</td>
        <!--  <td>{{ example.lat_lng_min }}</td>-->
              <td>
                {{undergrounds
                  .filter((item) => item.value === example.undergrounds)
                  .map(e => e.text)[0]
                }}
              </td>
              <td>
                {{ example.time }}
                <span v-if="example.transportType==='transport'">транспортом</span>
                <span v-else-if="example.transportType==='walk'">пешком</span>
                <span v-else>-</span>
              </td>
              <td>{{ example.description }}</td>
              <td>{{ example.predict }}</td>
              <td>
                <div class="btn-group" role="group">
                  <button
                          type="button"
                          class="btn btn-warning btn-sm"
                          v-b-modal.example-modal
                          @click="editExample(example)">
                      Скопировать
                  </button>
                  <button
                          type="button"
                          class="btn btn-danger btn-sm"
                          @click="onDeleteExample(example)">
                      Удалить
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <b-modal ref="addExampleModal"
             id="example-modal"
             title="Добавьте объект для прогноза стоимости аренды"
             size="lg"
             hide-footer>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
        <b-row>
          <b-col sm="3">
            <b-form-group id="form-roomsCount-group"
                        label="Количество комнат:"
                        label-for="form-roomsCount-input">
              <b-form-input id="form-roomsCount-input"
                            type="text"
                            v-model="$v.addApartmentForm.roomsCount.$model"
                            :state="validateState('roomsCount')"
                            aria-describedby="input-roomsCount-feedback">
              </b-form-input>
              <b-form-invalid-feedback id="input-roomsCount-feedback">
                Значение от 1 до 10
              </b-form-invalid-feedback>
            </b-form-group>
          </b-col>
          <b-col sm="9">
            <b-form-group id="form-undergrounds-group"
                        label="Метро:">
              <b-form-select v-model="addApartmentForm.undergrounds"
                             :options="undergrounds">
              </b-form-select>
            </b-form-group>
          </b-col>
        </b-row>
        <b-row>
          <b-col sm="4">
            <b-form-group id="form-totalArea-group"
                    label="Общая площадь:"
                    label-for="form-totalArea-input">
              <b-form-input id="form-totalArea-input"
                            type="text"
                            v-model="$v.addApartmentForm.totalArea.$model"
                            :state="validateState('totalArea')"
                            aria-describedby="input-totalArea-feedback">
              </b-form-input>
              <b-form-invalid-feedback id="input-totalArea-feedback">
                Значение от 15 до 150
              </b-form-invalid-feedback>
            </b-form-group>
          </b-col>
          <b-col sm="4">
            <b-form-group id="form-kitchenArea-group"
                    label="Площадь кухни:"
                    label-for="form-kitchenArea-input">
              <b-form-input id="form-kitchenArea-input"
                            type="text"
                            v-model="addApartmentForm.kitchenArea">
              </b-form-input>
            </b-form-group>
          </b-col>
          <b-col sm="4">
            <b-form-group id="form-livingArea-group"
                    label="Жилая площадь:"
                    label-for="form-livingArea-input">
              <b-form-input id="form-livingArea-input"
                            type="text"
                            v-model="addApartmentForm.livingArea">
              </b-form-input>
            </b-form-group>
          </b-col>
        </b-row>
        <b-form-group id="form-floorNumber-group"
                    label="Этаж / этажность:"
                    label-for="form-floorNumber-input">
          <b-row>
            <b-col sm="3">
              <b-form-input id="form-floorNumber-input"
                            type="text"
                            v-model="addApartmentForm.floorNumber"
                            placeholder="этаж">
              </b-form-input>
            </b-col>
            <b-col sm="3">
              <b-form-input id="form-floorsCount-input"
                            type="text"
                            v-model="addApartmentForm.floorsCount"
                            placeholder="этажность">
              </b-form-input>
            </b-col>
          </b-row>
        </b-form-group>
        <b-form-group id="form-time-group"
                    label="Время до метро:"
                    label-for="form-time-input">
          <b-row>
            <b-col sm="3">
              <b-form-input id="form-time-input"
                            type="text"
                            v-model="addApartmentForm.time">
              </b-form-input>
            </b-col>
            <b-col sm="3">
              <b-form-radio
                            name="transportType"
                            v-model="addApartmentForm.transportType"
                            value="walk">Пешком
              </b-form-radio>
              <b-form-radio
                            name="transportType"
                            v-model="addApartmentForm.transportType"
                            value="transport">Транспортом
              </b-form-radio>
            </b-col>
          </b-row>
        </b-form-group>
        <b-form-group id="form-description-group"
                    label="Описание:"
                    label-for="form-description-input">
          <b-form-textarea
            id="form-description-input"
            max-rows="6"
            placeholder="Описание квартиры..."
            rows="3"
            v-model="addApartmentForm.description">
          </b-form-textarea>
        </b-form-group>
        <b-button type="submit" variant="primary">Получить прогноз стоимости аренды!</b-button>
          &nbsp;&nbsp;
        <b-button type="reset" variant="danger">Очистить форму</b-button>
      </b-form>
    </b-modal>
  </div>
</template>

<script>
import axios from 'axios';
import { validationMixin } from 'vuelidate';
import { required, minLength, between } from 'vuelidate/lib/validators';
import Alert from './Alert.vue';
import undergrounds from './undergrounds.json';

export default {
  mixins: [validationMixin],
  data() {
    return {
      examples: [],
      addApartmentForm: {
        date: '',
        roomsCount: '',
        totalArea: '',
        kitchenArea: '',
        livingArea: '',
        floorNumber: '',
        floorsCount: '',
        lat_lng_min: '',
        undergrounds: '',
        transportType: '',
        time: '',
        description: '',
        predict: '',
      },
      undergrounds,
      message: '',
      showMessage: false,
    };
  },
  components: {
    alert: Alert,
  },
  validations: {
    addApartmentForm: {
      roomsCount: {
        required,
        between: between(1, 10),
      },
      totalArea: {
        required,
        between: between(15, 150),
      },
      description: {
        minLength: minLength(1),
      },
    },
  },
  methods: {
    validateState(name) {
      const { $dirty, $error } = this.$v.addApartmentForm[name];
      return $dirty ? !$error : null;
    },
    getExamples() {
      const path = 'http://localhost:5000/get-examples';
      axios.get(path)
        .then((res) => {
          this.examples = res.data.examples;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    addExample(payload) {
      const path = 'http://localhost:5000/predict';
      axios.post(path, payload)
        .then((resp) => {
          this.getExamples();
          this.message = `Прогноз стоимости аренды: ${resp.data.predictions} руб/мес.`;
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getExamples();
        });
    },
    initForm() {
      this.addApartmentForm.roomsCount = '';
      this.addApartmentForm.totalArea = '';
      this.addApartmentForm.kitchenArea = '';
      this.addApartmentForm.livingArea = '';
      this.addApartmentForm.floorNumber = '';
      this.addApartmentForm.floorsCount = '';
      this.addApartmentForm.undergrounds = '';
      this.addApartmentForm.transportType = '';
      this.addApartmentForm.time = '';
      this.addApartmentForm.description = '';
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$v.addApartmentForm.$touch();
      if (this.$v.addApartmentForm.$anyError) {
        return;
      }
      this.$refs.addExampleModal.hide();
      // let read = false;
      // if (this.addApartmentForm.read[0]) read = true;
      const payload = {
        roomsCount: this.addApartmentForm.roomsCount,
        totalArea: this.addApartmentForm.totalArea,
        kitchenArea: this.addApartmentForm.kitchenArea,
        livingArea: this.addApartmentForm.livingArea,
        floorNumber: this.addApartmentForm.floorNumber,
        floorsCount: this.addApartmentForm.floorsCount,
        lat_lng_min: '',
        undergrounds: this.addApartmentForm.undergrounds,
        transportType: this.addApartmentForm.transportType,
        time: this.addApartmentForm.time,
        description: this.addApartmentForm.description,
      };
      this.addExample(payload);
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addExampleModal.hide();
      this.initForm();
    },
    editExample(example) {
      this.addApartmentForm = example;
    },
    deleteExample(itemID) {
      const path = `http://localhost:5000/delete/${itemID}`;
      axios.delete(path)
        .then(() => {
          this.getExamples();
          this.message = 'Запись об объекте удалена!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getExamples();
        });
    },
    onDeleteExample(example) {
      this.deleteExample(example.id);
    },
  },
  created() {
    this.getExamples();
  },
};
</script>
