<script setup lang="ts">
  import { ref, type Ref } from 'vue'
  import axios from 'axios'
  import { VDataTableServer } from 'vuetify/labs/VDataTable'
import { computed } from 'vue';

  declare var require: any

  const messages = ref<{id: number, content: string}[]>([]);
  const numMessages = ref(0);
  const messagesPerPage = ref(10);
  const headers = ref([
    { title: 'ID', key: 'id',  align: 'start' },
    { title: 'Content', key: 'content', align: 'start' },
    { title: 'Actions', key: 'actions', sortable: false }
  ]);
  const search = ref("");
  const loading = ref(false);
  const isMessageDialogueOpen = ref(false);
  const isDeleteDialogueOpen = ref(false);
  const editIndex = ref(-1);
  const editedMessage: Message = ref({
    id: -1,
    content: ""
  })
  const defaultMessage: Message = ref({
    content: ""
  })
  const formTitle = computed(() => {return editIndex.value === -1 ? "New Message" : 'Edit Message'})

  async function getMessages() {
    loading.value = true;
    axios.get('http://127.0.0.1:8000/messages')
      .then((response: {data: {id: number, content: string}[]}) => {
        console.error(response);
        messages.value = response.data;
      })
      .catch((error: any) => {
        console.log(error);
      })
      .finally(() => {
        numMessages.value = messages.value.length;
        loading.value = false;
      })
  };

  function confirmDeleteDialogue() {

  }

  function closeDeleteDialogue() {

  }

  function saveEditedMessage() {

  }

  function closeDialogue() {

  }

  function createMessage(message: Message) {
  }

  function deleteMessage(message: Message) {

  }

  function editMessage(message: Message) {

  }

  function annotateMessage(message: Message) {

  }
</script>


<template>
  <v-data-table-server
    v-model:items-per-page="messagesPerPage"
    :headers="headers"
    :items-length="numMessages"
    :items="messages"
    :loading="loading"
    :search="search"
    class="elevation-1"
    item-value="name"
    @update:options="getMessages"
  >
    <template v-slot:top>
      <v-toolbar flat>
        <v-toolbar-title>All Datasets</v-toolbar-title>
        <v-divider class="mx-4" inset vertical></v-divider>
        <v-spacer></v-spacer>
        <v-dialog v-model="isMessageDialogueOpen" max-width="500px">
          <template v-slot:activator="{ props }">
            <v-btn color="primary" dark class="mb-2" v-bind="props">
              New Message
            </v-btn>
          </template>
          <v-card>
            <v-card-title>
              <span class="text-h5">{{ formTitle }}</span>
            </v-card-title>

            <v-card-text>
              <v-container>
                <v-row>
                  <v-col cols="12" sm="6" md="4">
                    <v-text-field
                      v-model="editedMessage.content"
                      label="Content"
                    ></v-text-field>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>

            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="blue-darken-1" variant="text" @click="closeDialogue">
                Cancel
              </v-btn>
              <v-btn color="blue-darken-1" variant="text" @click="saveEditedMessage">
                Save
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
        <v-dialog v-model="isDeleteDialogueOpen" max-width="500px">
          <v-card>
            <v-card-title class="text-h5"
              >Are you sure you want to delete this item?</v-card-title
            >
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="blue-darken-1" variant="text" @click="closeDeleteDialogue"
                >Cancel</v-btn
              >
              <v-btn
                color="blue-darken-1"
                variant="text"
                @click="confirmDeleteDialogue"
                >OK</v-btn
              >
              <v-spacer></v-spacer>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-toolbar>
    </template>
    <template v-slot:item.actions="{ item }">
      <v-icon size="small" class="me-2" @click="editMessage(item)" icon="mdi-pencil"></v-icon>
      <v-icon size="small" @click="annotateMessage(item)" icon="mdi-clipboard-edit"></v-icon>
      <v-icon size="small" @click="deleteMessage(item)" icon="mdi-delete"></v-icon>
    </template>
    <template v-slot:no-data>
      <v-btn color="primary" @click="getMessages"> Load Messages </v-btn>
    </template>
  </v-data-table-server>
</template>
