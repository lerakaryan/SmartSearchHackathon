// interfaces/hint.interfaces.ts

export interface BaseHint {
  type: 'registry' | 'knowledge_base' | 'action';
}

// Реестр - Тип 1 (Контракт)
export interface RegistryHintType1 extends BaseHint {
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

// Реестр - Тип 2 (Контрактная система)
export interface RegistryHintType2 extends BaseHint {
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

// База знаний
export interface KnowledgeBaseHint extends BaseHint {
  type: 'knowledge_base';
  text: string;
  link: string;
}

// Действие
export interface ActionHint extends BaseHint {
  type: 'action';
  intents: {
    name: string;
    entities: {
      dates: string[];
      money: string[];
      name: string[];
      addr: string[];
    };
  };
}

export type Hint = RegistryHintType1 | RegistryHintType2 | KnowledgeBaseHint | ActionHint;