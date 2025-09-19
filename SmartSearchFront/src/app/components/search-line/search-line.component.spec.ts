import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SearchLineComponent } from './search-line.component';

describe('SearchLineComponent', () => {
  let component: SearchLineComponent;
  let fixture: ComponentFixture<SearchLineComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SearchLineComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SearchLineComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
