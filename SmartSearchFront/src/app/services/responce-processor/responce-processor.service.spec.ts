import { TestBed } from '@angular/core/testing';

import { ResponceProcessorService } from './responce-processor.service';

describe('ResponceProcessorService', () => {
  let service: ResponceProcessorService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ResponceProcessorService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
