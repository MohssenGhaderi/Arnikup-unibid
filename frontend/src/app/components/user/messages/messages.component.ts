import { Component, OnInit, ViewChild, ElementRef ,HostListener } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { UserService } from 'src/app/services/user.service';
import { SharingService } from 'src/app/services/sharing.service';
import { LiveUserService } from 'src/app/services/live-user.service';
import { LoadingComponent } from 'src/app/components/loading/loading.component';
import { ErrorComponent } from 'src/app/components/error/error.component';
import { SuccessComponent } from 'src/app/components/success/success.component';
import { Links } from 'src/app/links.component';
import { EditUserInformation } from 'src/app/models/user/information/edit.model';
import { State } from 'src/app/models/user/information/state.model';

@Component({
  selector: 'app-messages',
  templateUrl: './messages.component.html',
  styleUrls: ['./messages.component.css']
})
export class MessagesComponent implements OnInit {
  registerForm: FormGroup;
  editables : EditUserInformation;
  toggleMessageTypeMenu = false;
  submitted = false;
  Link = Links;
  selectedMessageType="موضوع پیام";
  subscription: any;
  current_date = new Date();

  @ViewChild(LoadingComponent) loading: LoadingComponent ;
  @ViewChild(ErrorComponent) error: ErrorComponent ;
  @ViewChild(SuccessComponent) success: SuccessComponent ;

  constructor(
    private el: ElementRef,
    public shared:SharingService,
    private service:UserService,
    private formBuilder: FormBuilder
  ) { }

  @HostListener('mouseenter') onMouseEnter() {
    this.shared.visibleProfile = true;
  }
  @HostListener('mouseleave') onMouseLeave() {
    this.shared.visibleProfile = false;
  }

  ngOnInit() {
    this.subscription = this.shared.getCloseMessageTypeEmitter().subscribe(result=>{
      this.selectedMessageType = result;
      this.toggleMessageTypeMenu = false;
      this.el.nativeElement.getElementsByClassName('accountProfile-type')[0].classList.add('accountProfile-type-highlited');
    });

    this.el.nativeElement.getElementsByClassName('editProfileContainer')[0].classList.add(this.shared.lastClass);

    this.registerForm = this.formBuilder.group({
      subject: [''],
      title: [''],
      message: [''],
    });

  }
  goBack(){
    this.shared.lastClass = "myCfnAnimation-slideleft";
    this.el.nativeElement.getElementsByClassName('editProfileContainer')[0].classList.add('myCfnAnimation-slideright-none');
    setTimeout(()=>{
      this.shared.toggleMenu.messages = false;
      this.shared.toggleMenu.profile = true;
    },200);
  }

  toggleMessageType(eventDate){
    this.toggleMessageTypeMenu = true;
    eventDate.stopPropagation();
  }

  sendMessage(eventDate) {

    eventDate.preventDefault();
    this.submitted = true;
    if (this.registerForm.invalid) {
      return;
    }

    this.loading.show();

    var obj = {};

    if(this.selectedMessageType !="موضوع پیام")
      obj["subject"]=this.selectedMessageType;

    if(this.formFields.title.value)
      obj["title"]=this.formFields.title.value;

    if(this.formFields.message.value)
      obj["message"]=this.formFields.message.value;

    console.log(obj);
    this.service.SendMessage(obj).subscribe(result => {

      this.success.show(result,1500).
      then(()=>{
        this.loading.hide();
        this.toggleArchive();
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

  toggleArchive(){
    this.shared.toggleMenu.messageArchive = true;
    this.shared.toggleMenu.messages = false;
  }

  ngOnDestroy(){
    this.subscription.unsubscribe();
  }

  }
