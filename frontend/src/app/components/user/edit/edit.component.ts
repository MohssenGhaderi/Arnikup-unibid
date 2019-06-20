import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { UserService } from 'src/app/services/user.service';
import { SharingService } from 'src/app/services/sharing.service';
import { LiveUserService } from 'src/app/services/live-user.service';
import { LoadingComponent } from 'src/app/components/loading/loading.component';
import { ErrorComponent } from 'src/app/components/error/error.component';
import { SuccessComponent } from 'src/app/components/success/success.component';
import { Links } from 'src/app/links.component';
import { EditUserInformation } from 'src/app/models/user/information/edit.model'

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

  @ViewChild(LoadingComponent) loading: LoadingComponent ;
  @ViewChild(ErrorComponent) error: ErrorComponent ;
  @ViewChild(SuccessComponent) success: SuccessComponent ;

  constructor(private el: ElementRef, private shared:SharingService,private userService:UserService,private formBuilder: FormBuilder) { }

  ngOnInit() {
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
        state: [this.editables.state],
        address: [this.editables.address],
      });

      this.loading.hide();
    },
    error => {
      this.error.show(error,2000,'/signin');
    });
  }
  goBack(){
    this.shared.lastClass = "myCfnAnimation-slideleft";
    this.el.nativeElement.getElementsByClassName('editProfileContainer')[0].classList.add('myCfnAnimation-slideright-none');
    setTimeout(()=>{
      this.shared.toggleMenu.edit = false;
      this.shared.toggleMenu.profile = true;
    },200);
  }

  SaveProfile(eventDate) {
    eventDate.preventDefault();
    this.submitted = true;
    if (this.registerForm.invalid) {
      return;
    }

    this.loading.show();

    var obj = {
      "fullName":this.formFields.fullName.value,
      "email":this.formFields.email.value,
      "city":this.formFields.city.value,
      // "state":this.formFields.state.value,
      "state":1,
      "address":this.formFields.address.value,
    }

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

}
