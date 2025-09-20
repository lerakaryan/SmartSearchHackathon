export type ActionType = 
  | 'create_company_profile' 
  | 'add_ecp' 
  | 'create_direct_procurement'
  | 'update_user_profile' 
  | 'create_quotation_session'
  | 'create_contract' 
  | 'manage_offer';

export interface FieldConfig {
  key: string;
  label: string;
  type: 'text' | 'email' | 'number' | 'date' | 'textarea' | 'select' | 'file';
  required: boolean;
  options?: string[]; // для select
}

export interface ActionConfig {
  type: ActionType;
  title: string;
  description: string;
  fields: FieldConfig[];
}