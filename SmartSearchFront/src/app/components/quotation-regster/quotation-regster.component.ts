import { Component, OnInit } from '@angular/core';
import { RegistryHintType2 } from '../../interfaces/hint'; 


@Component({
  selector: 'app-quotation-regster',
  imports: [],
  templateUrl: './quotation-regster.component.html',
  styleUrl: './quotation-regster.component.css'
})
export class QuotationRegsterComponent implements OnInit { // Реализуем OnInit
     registryHintData: RegistryHintType2 | undefined; // Свойство для хранения данных (может быть undefined, пока данные не получены)

     ngOnInit(): void {
       // Здесь вы можете получить данные, например, из сервиса или жестко закодировать
       this.registryHintData = { // Заполняем данными
         type: 'registry',
         hintType: 2,
         data: {
           ksName: 'Название закупки',
           ksId: '12345',
           ksAmount: '100000',
           creationDate: '2024-01-15',
           completionDate: '2024-12-31',
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

