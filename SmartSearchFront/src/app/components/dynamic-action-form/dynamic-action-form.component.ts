import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { FormGroup, FormBuilder, Validators, ReactiveFormsModule } from '@angular/forms';
import { ActionConfigService } from '../../services/search-service/action-config.service';
import { ActionConfig, ActionType } from '../../models/action-type';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-dynamic-action-form',
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './dynamic-action-form.component.html',
  styleUrl: './dynamic-action-form.component.css'
})
export class DynamicActionFormComponent  implements OnInit {
  @Input() actionType!: ActionType;
  @Input() prefillData: any = {};
  @Output() formSubmit = new EventEmitter<any>();
  @Output() formCancel = new EventEmitter<void>();

  actionConfig!: ActionConfig;
  dynamicForm!: FormGroup;
  isLoading = true;

  constructor(
    private fb: FormBuilder,
    private actionConfigService: ActionConfigService
  ) {}

  ngOnInit(): void {
    this.loadFormConfig();
  }

  private loadFormConfig(): void {
    const config = this.actionConfigService.getConfig(this.actionType);
    if (config) {
      this.actionConfig = config;
      this.createForm();
      this.prefillForm();
      this.isLoading = false;
    }
  }

  private createForm(): void {
    const formGroup: any = {};

    this.actionConfig.fields.forEach(field => {
      const validators = field.required ? [Validators.required] : [];
      formGroup[field.key] = ['', validators];
    });

    this.dynamicForm = this.fb.group(formGroup);
  }

  private prefillForm(): void {
    if (this.prefillData) {
      this.dynamicForm.patchValue(this.prefillData);
    }
  }

  onFileChange(event: any, fieldKey: string): void {
    const file = event.target.files[0];
    if (file) {
      this.dynamicForm.get(fieldKey)?.setValue(file);
    }
  }

  onSubmit(): void {
    if (this.dynamicForm.valid) {
      this.formSubmit.emit(this.dynamicForm.value);
    } else {
      this.markFormGroupTouched();
    }
  }

  onCancel(): void {
    this.formCancel.emit();
  }

  private markFormGroupTouched(): void {
    Object.keys(this.dynamicForm.controls).forEach(key => {
      this.dynamicForm.get(key)?.markAsTouched();
    });
  }

  isFieldInvalid(fieldKey: string): boolean {
    const control = this.dynamicForm.get(fieldKey);
    return !!control && control.invalid && control.touched;
  }
}