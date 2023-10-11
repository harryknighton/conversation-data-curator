<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import { ref } from 'vue'


  const routes = ref([
    { path: "/", title: "Home" },
    { path: "/messages", title: "Messages" },
    { path: "/codes", title: "Codes" },
  ])
</script>

<template>
  <v-app>
    <v-app-bar title="Conversation Data Curator" />
    <v-navigation-drawer>
      <v-list-item v-for="route in routes" :title="route.title" :to="route.path"/>
    </v-navigation-drawer>
    <v-main>
      <RouterView/>
    </v-main>
  </v-app>
</template>
