import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DynamicActionFormComponent } from './dynamic-action-form.component';

describe('DynamicActionFormComponent', () => {
  let component: DynamicActionFormComponent;
  let fixture: ComponentFixture<DynamicActionFormComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DynamicActionFormComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DynamicActionFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
