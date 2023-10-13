interface Message {
  id: number,
  content: string,
}

interface Code {
  id: number,
  code: string,
}

interface Sorting {
  key: string,
  order: string,
}

interface Annotation {
  id: number,
  start_idx: number,
  end_idx: number,
  code_id: number,
  message_id: number,
}

interface AnnotationWithCode {
  id: number,
  start_idx: number,
  end_idx: number,
  code_id: number,
  message_id: number,
  code: string,
}
