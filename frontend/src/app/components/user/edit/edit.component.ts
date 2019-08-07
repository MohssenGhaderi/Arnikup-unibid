import { Component, OnInit, ViewChild, ElementRef ,HostListener } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { UserService } from 'src/app/services/user.service';
import { SharingService } from 'src/app/services/sharing.service';
import { LiveUserService } from 'src/app/services/live-user.service';
import { LoadingComponent } from 'src/app/components/loading/loading.component';
import { ErrorComponent } from 'src/app/components/error/error.component';
import { SuccessComponent } from 'src/app/components/success/success.component';
import { Links } from 'src/app/links.component';
import { EditUserInformation } from 'src/app/models/user/information/edit.model'
import { State } from 'src/app/models/user/information/state.model'

@Component({
  selector: 'app-edit-user',
  templateUrl: './edit.component.html',
  styleUrls: ['./edit.component.css']
})
export class EditUserComponent implements OnInit {

  registerForm: FormGroup;
  editables : EditUserInformation;
  submitted = false;
  Link = Links;
  selectedState:State;
  subscription: any;

  @ViewChild(LoadingComponent) loading: LoadingComponent ;
  @ViewChild(ErrorComponent) error: ErrorComponent ;
  @ViewChild(SuccessComponent) success: SuccessComponent ;

  constructor(
    private el: ElementRef,
    public shared:SharingService,
    private userService:UserService,
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
      console.log(result);
      this.selectedState = result;
    });

    this.el.nativeElement.getElementsByClassName('editProfileContainer')[0].classList.add('myCfnAnimation-slideright');


    this.registerForm = this.formBuilder.group({
      fullName: [''],
      email: [''],
      city: [''],
      state: [''],
      address: [''],
    });

    this.loading.show();
    this.userService.GetEditableInformation().subscribe(result =>{
      this.editables = result;

      this.registerForm = this.formBuilder.group({
        fullName: [this.editables.fullName],
        email: [this.editables.email],
        city: [this.editables.city],
        state: [this.editables.state? this.editables.state.title : 'انتخاب استان' ],
        address: [this.editables.address],
      });
      this.selectedState = this.editables.state ? this.editables.state :{"title":'انتخاب استان',"stateId":0};
      this.loading.hide();
    },
    error => {
      this.error.show(error,2000,'/signin');
    });
  }
  goBack(){
    this.liveUser.getProfileStatus();
    this.shared.lastClass = "myCfnAnimation-slideleft";
    this.el.nativeElement.getElementsByClassName('editProfileContainer')[0].classList.add('myCfnAnimation-slideright-none');
    setTimeout(()=>{
      this.shared.toggleMenu.edit = false;
      this.shared.toggleMenu.profile = true;
    },200);
  }

  SaveProfile(eventDate) {
    this.liveUser.getProfileStatus();
    this.liveUser.getStatus();
    eventDate.preventDefault();
    this.submitted = true;
    if (this.registerForm.invalid) {
      return;
    }

    this.loading.show();

    var obj = {
      "fullName":this.formFields.fullName.value,
      "email":this.formFields.email.value
    }

    if(this.selectedState.stateId != 0)
      obj["state"]=this.selectedState.stateId;

    if(this.formFields.city.value)
      obj["city"]=this.formFields.city.value;

    if(this.formFields.address.value)
      obj["address"]=this.formFields.address.value;


    this.userService.SetEditableInformation(obj).subscribe(result => {

      this.success.show(result,1500).
      then(()=>{
        this.loading.hide();
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
