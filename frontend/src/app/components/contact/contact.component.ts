import { Component, OnInit, ViewChild, ElementRef, Renderer2 } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { MainServices } from 'src/app/services/main.service';
import { SharingService } from 'src/app/services/sharing.service';
import { GuestMessage } from 'src/app/models/guestMessage.model';
import { LoadingComponent } from 'src/app/components/loading/loading.component';
import { ErrorComponent } from 'src/app/components/error/error.component';
import { SuccessComponent } from 'src/app/components/success/success.component';

@Component({
  selector: 'contact-about',
  templateUrl: './contact.component.html',
  styleUrls: ['./contact.component.css']
})
export class ContactComponent implements OnInit {

  @ViewChild('mainWrapper') mainWrapperElem: ElementRef;
  @ViewChild(LoadingComponent ) loading: LoadingComponent ;
  @ViewChild(ErrorComponent) error: ErrorComponent ;
  @ViewChild(SuccessComponent) success: SuccessComponent ;
  registerForm: FormGroup;
  editables : GuestMessage;
  selectedSendType = "موبایل";
  subscription: any;

  constructor(
    public shared:SharingService,
    private service:MainServices,
    private renderer: Renderer2,
    private formBuilder: FormBuilder
  ){ }

  ngOnInit() {

    const wrapperElem: HTMLElement = document.getElementById('mainWrapper');
    this.renderer.setStyle(wrapperElem, 'justify-content', 'initial');
    this.renderer.setStyle(wrapperElem, 'align-items', 'initial');
    this.shared.toggleMenu.reset();

    this.subscription = this.shared.getChangeGuestMessageTypeEmitter().subscribe(result=>{
      this.selectedSendType = result;
    });

    this.registerForm = this.formBuilder.group({
      fullName: [''],
      email: [''],
      mobile: [''],
      sendType: [''],
      message: [''],
    });
  }

  sendMessage(eventDate) {

    if (this.registerForm.invalid) {
      var msg = "لطفا در ورود اطلاعات فرم دقت کنید."
      this.error.show({"error":{"message":msg}},3000,null);
      return;
    }

    eventDate.preventDefault();

    this.loading.show();

    var obj = {"sendType":this.selectedSendType};

    if(this.formFields.fullName.value)
      obj["fullName"]=this.formFields.fullName.value;

    if(this.formFields.email.value)
      obj["email"]=this.formFields.email.value;

    if(this.formFields.mobile.value)
      obj["mobile"]=this.formFields.mobile.value;

    if(this.formFields.message.value)
      obj["message"]=this.formFields.message.value;

    this.service.SendGuestMessage(obj).subscribe(result => {

      this.success.show(result,1500).
      then(()=>{
        this.loading.hide();
        this.registerForm = this.formBuilder.group({
          fullName: [''],
          email: [''],
          mobile: [''],
          sendType: [''],
          message: [''],
        });
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

}
