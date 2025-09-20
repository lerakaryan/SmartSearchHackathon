// interfaces/hint.interfaces.ts

export interface SearchResponse {
  registry_records: RegistryHint[];
  knowledge_base_articles: KnowledgeBaseHint[];
  intents: ActionHintIntents;
}

export interface ActionHintIntents {
  name: string;
  entities: {
    names: string;
    // добавьте другие поля если необходимо
  };
}

export interface RegistryHint {
  type: 'registry';
  hintType: 1 | 2;
  data: RegistryHintType1['data'] | RegistryHintType2['data'];
}

// Остальные интерфейсы остаются
export interface BaseHint {
  type: 'registry' | 'knowledge_base' | 'action';
}

export interface RegistryHintType1 {
  type: 'registry';
  hintType: 1;
  data: {
    contractName: string;
    contractId: string;
    contractAmount: string;
    contractDate: string;
    category: string;
    customerName: string;
    customerINN: string;
    supplierName: string;
    supplierINN: string;
    lawBasis: string;
  };
}

export interface RegistryHintType2 {
  type: 'registry';
  hintType: 2;
  data: {
    ksName: string;
    ksId: string;
    ksAmount: string;
    creationDate: string;
    completionDate: string;
    category: string;
    customerName: string;
    customerINN: string;
    supplierName: string;
    supplierINN: string;
    lawBasis: string;
  };
}

export interface KnowledgeBaseHint {
  type: 'knowledge_base';
  text: string;
  link: string;
}

export interface ActionHint {
  type: 'action';
  intents: ActionHintIntents;
}