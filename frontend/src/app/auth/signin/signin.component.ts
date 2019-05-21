import { Component, OnInit, ViewChild, ElementRef, Renderer2 } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { AuthenticationService } from 'src/app/_services/authentication.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-signin',
  templateUrl: './signin.component.html',
  styleUrls: ['./signin.component.css']
})
export class SigninComponent implements OnInit {
  loginForm: FormGroup;
  loading = false;
  submitted = false;
  errorObj = '';
  timeoutId;
  @ViewChild('errorMessage') errorMessageElem: ElementRef;
  constructor(private formBuilder: FormBuilder,
              private authenticationService: AuthenticationService,
              private router: Router,
              private renderer: Renderer2) {
                const currentUser = localStorage.getItem('currentUser');
                if (currentUser) {
                  this.router.navigate(['/']);
                }
              }

  ngOnInit() {
    this.loginForm = this.formBuilder.group({
      username: ['', Validators.required],
      password: ['', Validators.required]
    });
    const wrapperElem: HTMLElement = document.getElementById('mainWrapper');
    this.renderer.setStyle(wrapperElem, 'justify-content', 'center');
    this.renderer.setStyle(wrapperElem, 'align-items', 'center');
  }

  onSubmit() {
    this.submitted = true;
    if (this.loginForm.invalid) {
      return;
    }

    this.loading = true;

    this.authenticationService.login(this.formFields.username.value, this.formFields.password.value).subscribe(user => {
      localStorage.setItem('currentUser', JSON.stringify(user));
      this.router.navigate(['/']);
    },
    error => {
      this.errorObj = error;
      this.loading = false;
      if (error.error.reason === 'verification') {
        this.router.navigate(['/verification']);
      }
      this.errorMessageElem.nativeElement.classList.add('cfnAnimation-fadeIn');
      clearTimeout(this.timeoutId);
      this.timeoutId = setTimeout(() => {
        this.errorMessageElem.nativeElement.classList.remove('cfnAnimation-fadeIn');
      }, 5000);
    });
  }

  get formFields() {
    return this.loginForm.controls;
  }

}
