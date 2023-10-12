<script setup lang="ts">
  import { ref, type Ref } from 'vue'
  import axios from 'axios'
  import CRUDTable from '../components/CRUDTable.vue'
  import { API_URL } from '@/main';


  const codes: Ref<Code[]> = ref([]);
  const headers = ref([
    { title: 'ID', key: 'id',  align: 'start', useInForm: false },
    { title: 'Code', key: 'code', align: 'start', useInForm: true },
    { title: 'Actions', key: 'actions', sortable: false, useInForm: false }
  ]);
  const loading = ref(false);
  const title = "All Codes"
  const sortBy = ref([{key: 'code', order: 'asc'}]);
  const defaultCode: Code = {  // Default code to restore the input to
    id: -1,
    code: ""
  }


  // Database CRUD operations
  function createCode(code: Code) : void {
    axios.post(API_URL + 'codes/create/', { code: code.code })
      .then((response: { data: Code }) => {
        codes.value.push(response.data);
      })
      .catch((error: any) => {
        console.error(error);
      })
  }

  async function getCodes(search: string, sortBy: Sorting[]) {
    loading.value = true;
    let params = {
      search: search,
      sort_by: sortBy.length > 0 ? sortBy[0].key : 'code',
      sort_asc: sortBy.length > 0 ? sortBy[0].order === 'asc': true,
    }
    axios.get(API_URL + 'codes/', { params })
      .then(
        (response: {data: Code[]}) => {codes.value = response.data},
        () => {codes.value = []}
      )
      .catch((error: any) => {
        console.error(error);
      })
      .finally(() => {loading.value = false;})
  };

  async function deleteCode(code: Code) {
    axios.post(API_URL + 'codes/delete/', { code: code.code })
      .then(() => {
        codes.value.splice(codes.value.indexOf(code), 1);
      })
      .catch((error: any) => {
        console.error(error);
    })

  }

  async function updateCode(code: Code) {
    const codeIndex = codes.value.findIndex(item => item.id === code.id);
    codes.value[codeIndex] = code
    axios.post(API_URL + 'codes/update/', { ...code })
      .catch((error: any) => {
        console.error(error);
      })

  }
</script>


<template>
  <CRUDTable
    @createItem="createCode"
    @fetchItems="getCodes"
    @editItem="updateCode"
    @deleteItem="deleteCode"
    :items="codes"
    :title="title"
    :headers="headers"
    :loading="loading"
    :defaultItem="defaultCode"
    :sortBy="sortBy"
  >
  </CRUDTable>
</template>
