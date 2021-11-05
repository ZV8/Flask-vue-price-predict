import Vue from 'vue';
import Router from 'vue-router';
import PredictForm from '../components/PredictForm.vue';
import Ping from '../components/Ping.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'PredictForm',
      component: PredictForm,
    },
    {
      path: '/ping',
      name: 'Ping',
      component: Ping,
    },
  ],
});
