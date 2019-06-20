import { Component, OnInit, ViewChild , ElementRef} from '@angular/core';
import { Router } from '@angular/router';
import { AuthenticationService } from 'src/app/services/authentication.service';


@Component({
  selector: 'app-error',
  templateUrl: './error.component.html',
  styleUrls: ['./error.component.css']
})
export class ErrorComponent implements OnInit {

  errorObj = null;
  timeoutId;

  @ViewChild('errorMessage') errorMessageElem: ElementRef;
  constructor(
    private router:Router,
    private authService:AuthenticationService,
  )
  {}

  ngOnInit() {
  }

  show(error,time=2000,navigate=null): Promise<void> {
    return new Promise((resolve, reject) => {
      this.errorObj = error;
      this.errorMessageElem.nativeElement.classList.remove('cfnAnimation-fadeOut');
      this.errorMessageElem.nativeElement.classList.add('cfnAnimation-fadeIn');
      clearTimeout(this.timeoutId);
      this.timeoutId = setTimeout(() => {
        this.errorMessageElem.nativeElement.classList.add('cfnAnimation-fadeOut');
        if(error.status==401){
          this.authService.logout();
          this.router.navigate(['/signin']);
        }
        if(navigate){
          this.router.navigate([navigate]);
        }
        resolve();
      }, time);
    })
  }
}
