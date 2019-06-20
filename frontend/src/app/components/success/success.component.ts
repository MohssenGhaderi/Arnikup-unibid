import { Component, OnInit, ViewChild , ElementRef} from '@angular/core';
import { Router } from '@angular/router';
import { AuthenticationService } from 'src/app/services/authentication.service';


@Component({
  selector: 'app-success',
  templateUrl: './success.component.html',
  styleUrls: ['./success.component.css']
})
export class SuccessComponent implements OnInit {

  successObj = null;
  timeoutId;

  @ViewChild('successMessage') successMessageElem: ElementRef;
  constructor(
    private router:Router,
    private authService:AuthenticationService,
  )
  {}

  ngOnInit() {
  }

    show(object,time=2000): Promise<void> {
      return new Promise((resolve, reject) => {
        this.successObj = object;
        this.successMessageElem.nativeElement.classList.remove('cfnAnimation-fadeOut');
        this.successMessageElem.nativeElement.classList.add('cfnAnimation-fadeIn');
        clearTimeout(this.timeoutId);
        this.timeoutId = setTimeout(() => {
          this.successMessageElem.nativeElement.classList.add('cfnAnimation-fadeOut');
          resolve();
        }, time);
      })
  }
  
}
