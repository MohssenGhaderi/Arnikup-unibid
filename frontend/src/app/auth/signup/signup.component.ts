import { Component, OnInit, ViewChild, ElementRef, Renderer2 } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { AuthenticationService } from 'src/app/_services/authentication.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.css']
})
export class SignupComponent implements OnInit {

  registerForm: FormGroup;
  submitted = false;
  loading = false;
  errorObj = '';
  timeoutId;
  @ViewChild('errorMessage') errorMessageElem: ElementRef;
  constructor(private formBuilder: FormBuilder,
    private authenticationService: AuthenticationService,
    private router: Router,
    private renderer: Renderer2) { }

  ngOnInit() {
    this.registerForm = this.formBuilder.group({
      username: ['', Validators.required],
      password: ['', Validators.required],
      confirmPassword: ['', Validators.required],
      mobile: ['', Validators.required],
      invitor: [''],
    });

    const wrapperElem: HTMLElement = document.getElementById('mainWrapper');
    this.renderer.setStyle(wrapperElem, 'justify-content', 'center');
    this.renderer.setStyle(wrapperElem, 'align-items', 'center');
  }

  onSubmit() {
    this.submitted = true;
    if (this.registerForm.invalid) {
      return;
    }

    this.loading = true;

    this.authenticationService.register(this.formFields.username.value, this.formFields.password.value,
      this.formFields.confirmPassword.value, this.formFields.mobile.value,
      this.formFields.invitor.value).subscribe(result => {
      this.router.navigate(['/verification']);
    },
    error => {
      this.errorObj = error;
      this.loading = false;
      this.errorMessageElem.nativeElement.classList.add('cfnAnimation-fadeIn');
      clearTimeout(this.timeoutId);
      this.timeoutId = setTimeout(() => {
        this.errorMessageElem.nativeElement.classList.remove('cfnAnimation-fadeIn');
      }, 5000);
    });
  }

  get formFields() {
    return this.registerForm.controls;
  }

}
