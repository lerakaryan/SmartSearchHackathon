import { EventEmitter, Injectable, Input, Output } from '@angular/core';
import { ActionConfig, ActionType } from '../../models/action-type';
import { FormGroup } from '@angular/forms';

@Injectable({
  providedIn: 'root'
})
export class ActionConfigService{
   
  private configs: Map<ActionType, ActionConfig> = new Map();

  constructor() {
    this.initializeConfigs();
  }

  private initializeConfigs(): void {
    // Конфигурация для create_company_profile
    this.configs.set('create_company_profile', {
      type: 'create_company_profile',
      title: 'Создание профиля компании',
      description: 'Заполните информацию о вашей компании',
      fields: [
        { key: 'companyName', label: 'Название компании', type: 'text', required: true },
        { key: 'taxId', label: 'ИНН', type: 'text', required: true },
        { key: 'address', label: 'Адрес', type: 'text', required: false },
        { key: 'phone', label: 'Телефон', type: 'text', required: false },
        { key: 'email', label: 'Email', type: 'email', required: true }
      ]
    });

    // Конфигурация для add_ecp
    this.configs.set('add_ecp', {
      type: 'add_ecp',
      title: 'Добавление ЭЦП',
      description: 'Загрузите вашу электронную цифровую подпись',
      fields: [
        { key: 'ecpFile', label: 'Файл ЭЦП', type: 'file', required: true },
        { key: 'password', label: 'Пароль', type: 'text', required: true },
        { key: 'validUntil', label: 'Действительна до', type: 'date', required: false }
      ]
    });

    // Конфигурация для create_direct_procurement
    this.configs.set('create_direct_procurement', {
      type: 'create_direct_procurement',
      title: 'Создание прямой закупки',
      description: 'Заполните данные для прямой закупки',
      fields: [
        { key: 'procurementName', label: 'Название закупки', type: 'text', required: true },
        { key: 'description', label: 'Описание', type: 'textarea', required: false },
        { key: 'budget', label: 'Бюджет', type: 'number', required: true },
        { key: 'deadline', label: 'Срок выполнения', type: 'date', required: false }
      ]
    });

  }

  getConfig(actionType: ActionType): ActionConfig | undefined {
    return this.configs.get(actionType);
  }

  getAllActionTypes(): ActionType[] {
    return Array.from(this.configs.keys());
  }
}