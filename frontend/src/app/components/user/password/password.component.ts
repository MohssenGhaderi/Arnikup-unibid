import { Component, OnInit, ViewChild, ElementRef ,HostListener } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { AuthenticationService } from 'src/app/services/authentication.service';
import { SharingService } from 'src/app/services/sharing.service';
import { LiveUserService } from 'src/app/services/live-user.service';
import { LoadingComponent } from 'src/app/components/loading/loading.component';
import { ErrorComponent } from 'src/app/components/error/error.component';
import { SuccessComponent } from 'src/app/components/success/success.component';
import { Links } from 'src/app/links.component';
import { EditUserInformation } from 'src/app/models/user/information/edit.model';
import { State } from 'src/app/models/user/information/state.model';

@Component({
  selector: 'app-password',
  templateUrl: './password.component.html',
  styleUrls: ['./password.component.css']
})
export class PasswordComponent implements OnInit {
  registerForm: FormGroup;
  editables : EditUserInformation;
  submitted = false;
  Link = Links;
  selectedState:State;
  subscription: any;
  current_date = new Date();

  @ViewChild(LoadingComponent) loading: LoadingComponent ;
  @ViewChild(ErrorComponent) error: ErrorComponent ;
  @ViewChild(SuccessComponent) success: SuccessComponent ;

  constructor(
    private el: ElementRef,
    public shared:SharingService,
    private auth:AuthenticationService,
    private formBuilder: FormBuilder,
    private liveUser:LiveUserService,
  ) { }

  @HostListener('mouseenter') onMouseEnter() {
    this.shared.visibleProfile = true;
  }
  @HostListener('mouseleave') onMouseLeave() {
    this.shared.visibleProfile = false;
  }

  ngOnInit() {
    this.subscription = this.shared.getStateEmitter().subscribe(result=>{
      this.selectedState = result;
    });

    this.el.nativeElement.getElementsByClassName('editProfileContainer')[0].classList.add('myCfnAnimation-slideright');

    this.registerForm = this.formBuilder.group({
      oldPassword: [''],
      newPassword: [''],
      confirmPassword: [''],
      currentTime :['']
    });

  }
  goBack(){
    this.liveUser.getProfileStatus();
    this.shared.lastClass = "myCfnAnimation-slideleft";
    this.el.nativeElement.getElementsByClassName('editProfileContainer')[0].classList.add('myCfnAnimation-slideright-none');
    setTimeout(()=>{
      this.shared.toggleMenu.password = false;
      this.shared.toggleMenu.profile = true;
    },200);
  }

  ChangePassword(eventDate) {
    this.liveUser.getProfileStatus();
    this.liveUser.getStatus();
    eventDate.preventDefault();
    this.submitted = true;
    if (this.registerForm.invalid) {
      return;
    }

    this.loading.show();

    var obj = {"currentTime":this.formFields.currentTime.value};
    if(this.formFields.oldPassword.value)
      obj["oldPassword"]=this.formFields.oldPassword.value;
    if(this.formFields.newPassword.value)
      obj["newPassword"]=this.formFields.newPassword.value;
    if(this.formFields.confirmPassword.value)
      obj["confirmPassword"]=this.formFields.confirmPassword.value;

    this.auth.changePassword(obj).subscribe(result => {

      this.success.show(result,1500).
      then(()=>{
        this.loading.hide();
        this.auth.logout();
        this.goBack();
      });
    },
    error => {
      this.loading.hide();
      this.error.show(error,3000,null);
    });
  }

  get formFields() {
    return this.registerForm.controls;
  }
  toggleAvatar(){
    this.shared.toggleMenu.reset();
    this.shared.toggleMenu.avatar = true;
  }

  toggleStates(eventDate){
    this.shared.states = true;
    eventDate.stopPropagation();
  }

  ngOnDestroy(){
    this.subscription.unsubscribe();
  }

  }
