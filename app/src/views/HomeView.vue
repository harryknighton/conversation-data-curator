<template>
  <v-container fill-height fluid>
    <v-spacer></v-spacer>
    <v-row justify="center" align="center">
      <v-col cols="12" sm="8" md="4">
        <h1 class="text" id="title">Welcome!</h1>
        <p class="text" id="overview">
          This app was written for a take-home interview.
          It can be used to collect snippets of dialogue (messages) and annotate potentially overlapping portions of them with codes that indicate the function or importance of words.
        </p>
        <h2 class="text" id="start">Click on 'Messages' to get started!</h2>
      </v-col>
    </v-row>
</v-container>
</template>

<style>
  #overview {
    font-size: medium,
  }

  #start {
    font-size: medium
  }

</style>
