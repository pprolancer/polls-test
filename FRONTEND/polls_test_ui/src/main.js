import Vue from 'vue'
import App from './App.vue'
import packageJson from "../package.json";

Vue.config.productionTip = false
Vue.prototype.$appVersion = packageJson.version;

new Vue({
  render: h => h(App),
}).$mount('#app')
