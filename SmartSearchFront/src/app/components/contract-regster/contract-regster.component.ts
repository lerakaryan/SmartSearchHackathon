import { Component, OnInit } from '@angular/core';
import { RegistryHintType1 } from '../../interfaces/hint'; 


@Component({
  selector: 'app-contract-regster',
  imports: [],
  templateUrl: './contract-regster.component.html',
  styleUrl: './contract-regster.component.css'
})
export class QuotationRegsterComponent implements OnInit { // Реализуем OnInit
     registryHintData: RegistryHintType1 | undefined; // Свойство для хранения данных (может быть undefined, пока данные не получены)

     ngOnInit(): void {
       // Здесь вы можете получить данные, например, из сервиса или жестко закодировать
       this.registryHintData = { // Заполняем данными
         type: 'registry',
         hintType: 1,
         data: {
          contractName: 'Название контракта',
          contractId: '22345',
          contractAmount: '100000',
          contractDate: '2024-12-31',
          category: 'Категория',
          customerName: 'Заказчик',
          customerINN: '1234567890',
          supplierName: 'Поставщик',
          supplierINN: '0987654321',
          lawBasis: '44-ФЗ',
         },
       };
      }
    }

