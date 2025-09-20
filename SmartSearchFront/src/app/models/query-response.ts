export interface QueryResponse {
  id?: number;
  query: string;
  response: string;
  rating: number;
}

export interface QueryResponseWithId extends QueryResponse {
  id: number;
}