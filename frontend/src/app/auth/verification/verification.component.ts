import { Component, OnInit, ViewChild, ElementRef, Renderer2 } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthenticationService } from 'src/app/_services/authentication.service';
import { VerificationGet } from 'src/app/models/auth/verificationGet';
import { VerificationPut } from 'src/app/models/auth/verificationPut';
import { VerificationPost } from 'src/app/models/auth/verificationPost';

@Component({
  selector: 'app-verification',
  templateUrl: './verification.component.html',
  styleUrls: ['./verification.component.css']
})
export class VerificationComponent implements OnInit {
  verificationForm: FormGroup;
  submitted = false;
  loading = false;
  errorObj = '';
  timeoutId;
  errorTimeoutId;
  verficationGet: VerificationGet;
  verificationPut: VerificationPut;
  verificationPost: VerificationPost;
  disabled = false;
  @ViewChild('verificationText') verificationTextElm: ElementRef;
  @ViewChild('errorMessage') errorMessageElem: ElementRef;

  constructor(private formBuilder: FormBuilder,
    private authenticationService: AuthenticationService,
    private router: Router,
    private renderer: Renderer2) {
    }

  ngOnInit() {

    const wrapperElem: HTMLElement = document.getElementById('mainWrapper');
    this.renderer.setStyle(wrapperElem, 'justify-content', 'center');
    this.renderer.setStyle(wrapperElem, 'align-items', 'center');

    this.verificationForm = this.formBuilder.group({
      username: ['', Validators.required]
    });

      this.authenticationService.verifyPut({resend:false}).subscribe(result => {
        clearInterval(this.timeoutId);
        this.verificationPut = result;
        this.timeoutId = setInterval(() => {
          if(this.verificationPut.remainedToExpire <= 0){
            clearInterval(this.timeoutId)
            this.disabled = true;
          } else{
            this.verificationPut.remainedToExpire--;
          }
        }, 1000);
      },
      error => {
        this.errorObj = error;
        this.loading = false;
        this.errorMessageElem.nativeElement.classList.add('cfnAnimation-fadeIn');
        this.errorTimeoutId = setTimeout(() => {
          this.errorMessageElem.nativeElement.classList.remove('cfnAnimation-fadeIn');
          if (error.error.reason === 'retryLogin') {
            this.router.navigate(['/signin']);
          }
        }, 2000);
      });

  }

  onSubmit() {
    this.loading = true;
    if (this.verificationTextElm.nativeElement.textContent!=''){
      this.authenticationService.verifyPost({code:this.verificationTextElm.nativeElement.textContent}).subscribe(user => {
        localStorage.setItem('currentUser', JSON.stringify(user));
        this.router.navigate(['/']);
      },
      error => {
        this.errorObj = error;
        this.loading = false;
        this.errorMessageElem.nativeElement.classList.add('cfnAnimation-fadeIn');
        this.errorTimeoutId = setTimeout(() => {
          this.errorMessageElem.nativeElement.classList.remove('cfnAnimation-fadeIn');
          if (error.error.reason === 'retryLogin') {
            this.router.navigate(['/signin']);
          }
        }, 2000);
      });
    }
  }

  resendActivationCodeClick(eventData) {
    eventData.stopPropagation();
    this.authenticationService.verifyPut({resend:true}).subscribe(result => {
      clearInterval(this.timeoutId);
      this.disabled = false;
      this.verificationPut = result;
      this.timeoutId = setInterval(() => {
        if(this.verificationPut.remainedToExpire <= 0){
          clearInterval(this.timeoutId)
          this.disabled = true;
        } else{
          this.verificationPut.remainedToExpire--;
        }
      }, 1000);
    },
    error => {
      this.errorObj = error;
      this.loading = false;
      this.errorMessageElem.nativeElement.classList.add('cfnAnimation-fadeIn');
      this.errorTimeoutId = setTimeout(() => {
        this.errorMessageElem.nativeElement.classList.remove('cfnAnimation-fadeIn');
        if (error.error.reason === 'retryLogin') {
          this.router.navigate(['/signin']);
        }
      }, 2000);
    });
  }

}
