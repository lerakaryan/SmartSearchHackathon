import { TestBed } from '@angular/core/testing';

import { ActionConfigService } from './action-config.service';

describe('ActionConfigService', () => {
  let service: ActionConfigService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ActionConfigService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
