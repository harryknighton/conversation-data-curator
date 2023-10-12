import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import CRUDTable from './components/CRUDTable.vue'

// Vuetify
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import { md3 } from 'vuetify/blueprints'
import { aliases, mdi } from 'vuetify/iconsets/mdi'
import '@mdi/font/css/materialdesignicons.css'
import { VDataTableServer } from 'vuetify/labs/VDataTable'


export const API_URL = "http://127.0.0.1:8000/"

const vuetify = createVuetify({
  components,
  directives,
  blueprint: md3,
  icons: {
    defaultSet: 'mdi',
    aliases,
    sets: {
      mdi,
    },
  },
})

const app = createApp(App)

app.use(vuetify)
// app.use(createPinia())
app.use(router)

app.component('CRUDTable', CRUDTable)
app.component('VDataTableServer', VDataTableServer)

app.mount('#app')
