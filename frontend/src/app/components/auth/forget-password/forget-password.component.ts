import { Component, OnInit, ViewChild, ElementRef, Renderer2 } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { AuthenticationService } from 'src/app/services/authentication.service';
import { LoadingComponent } from 'src/app/components/loading/loading.component';
import { ErrorComponent } from 'src/app/components/error/error.component';
import { Router } from '@angular/router';
import { Location } from '@angular/common';
import { Links } from 'src/app/links.component';

@Component({
  selector: 'app-forget-password',
  templateUrl: './forget-password.component.html',
  styleUrls: ['./forget-password.component.css']
})
export class ForgetPasswordComponent implements OnInit {
  loginForm: FormGroup;
  submitted = false;
  errorObj = '';
  Link = Links;
  progress;
  userAvatar;
  timeoutId;
  @ViewChild(LoadingComponent) loading: LoadingComponent ;
  @ViewChild(ErrorComponent) error: ErrorComponent ;

  constructor(private formBuilder: FormBuilder,
              private location: Location,
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
      forgotField: ['', Validators.required]
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

    this.loading.show();

    this.authenticationService.forgotPassword({"forgotField":this.formFields.forgotField.value}).subscribe(result => {
      this.router.navigate(['/signin']);
    },
    error => {
      this.loading.hide();
      this.error.show(error,3000,null)
    });
  }

  get formFields() {
    return this.loginForm.controls;
  }

}
