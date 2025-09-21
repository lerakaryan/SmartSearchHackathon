import { ComponentFixture, TestBed } from '@angular/core/testing';

import { QuotationRegsterComponent } from './contract-regster.component';

describe('QuotationRegsterComponent', () => {
  let component: QuotationRegsterComponent;
  let fixture: ComponentFixture<QuotationRegsterComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [QuotationRegsterComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(QuotationRegsterComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
