<script setup lang="ts">
  import { ref, type Ref } from 'vue'
  import axios from 'axios'
  import CRUDTable from '../components/CRUDTable.vue'
  import { API_URL } from '@/main';
  import { useRoute } from 'vue-router';

  const route = useRoute()

  const props = defineProps<{
    messageContent: string,
  }>()

  const annotations: Ref<AnnotationWithCode[]> = ref([]);
  const headers = ref([
    { title: 'ID', key: 'id',  align: 'start', useInForm: false },
    { title: 'Start Idx', key: 'start_idx', align: 'start', useInForm: true },
    { title: 'End Idx', key: 'end_idx', align: 'start', useInForm: true },
    { title: 'Code ID', key: 'code_id', align: 'start', useInForm: true },
    { title: 'Code', key: 'code', sortable: true, align: 'start', useInForm: false },
    { title: 'Actions', key: 'actions', useInForm: false }
  ]);
  const loading = ref(false);
  const title = props.messageContent;
  const sortBy = ref([{key: 'code', order: 'asc'}]);
  const defaultAnnotation: AnnotationWithCode = {  // Default to restore the input annotation to
    id: -1,
    start_idx: -1,
    end_idx: -1,
    code_id: -1,
    message_id: -1,
    code: "",
  }


  // Database CRUD operations
  function createAnnotation(annotation: AnnotationWithCode) : void {
    const params = {
      message_id: route.params.messageID,
      code_id: annotation.code_id,
      start_idx: annotation.start_idx,
      end_idx: annotation.end_idx,
    }
    axios.post(API_URL + `annotations/${route.params.messageID}/create/`, params)
      .then((response: { data: [Annotation, Code] }) => {
        annotations.value.push({...response.data[1], ...response.data[0]});
      })
      .catch((error: any) => {
        console.error(error);
      })
  }

  async function getAnnotations() {
    loading.value = true;
    axios.get(API_URL + `annotations/${route.params.messageID}/`)
      .then(
        (response: {data: {result: [Annotation, Code]}[]}) => {
          annotations.value = response.data.map((item) => {
            return {...item.result[1], ...item.result[0]}})
        },
        () => {annotations.value = []}
      )
      .catch((error: any) => {
        console.error(error);
      })
      .finally(() => {loading.value = false;})
  };

  async function updateAnnotation(annotation: AnnotationWithCode) {
    const annotationIndex = annotations.value.findIndex(item => item.id === annotation.id);
    annotations.value[annotationIndex] = annotation;
    axios.post(API_URL + 'annotations/update/', { ...annotation })
      .catch((error: any) => {
        console.error(error);
      })

  }

  async function deleteAnnotation(annotation: AnnotationWithCode) {
    axios.post(API_URL + 'annotations/delete/', { id: annotation.id })
      .then(() => {
        annotations.value.splice(annotations.value.indexOf(annotation), 1);
      })
      .catch((error: any) => {
        console.error(error);
    })

  }

</script>


<template>
  <CRUDTable
    @createItem="createAnnotation"
    @fetchItems="getAnnotations"
    @deleteItem="deleteAnnotation"
    @editItem="updateAnnotation"
    :items="annotations"
    :title="title"
    :headers="headers"
    :loading="loading"
    :defaultItem="defaultAnnotation"
    :sortBy="sortBy"
  >
  </CRUDTable>
</template>
