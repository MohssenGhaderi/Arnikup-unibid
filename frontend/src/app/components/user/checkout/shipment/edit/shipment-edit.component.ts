import { Component, OnInit, ViewChild, ElementRef ,HostListener } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { LoadingComponent } from 'src/app/components/loading/loading.component';
import { ErrorComponent } from 'src/app/components/error/error.component';
import { SuccessComponent } from 'src/app/components/success/success.component';
import { UserService } from 'src/app/services/user.service';
import { SharingService } from 'src/app/services/sharing.service';
import { Links } from 'src/app/links.component';
import { ShipmentInformation } from 'src/app/models/user/information/shipment.model'
import { State } from 'src/app/models/user/information/state.model'

@Component({
  selector: 'app-shipment-edit',
  templateUrl: './shipment-edit.component.html',
  styleUrls: ['./shipment-edit.component.css']
})
export class ShipmentEditComponent implements OnInit {
  @ViewChild(LoadingComponent) loading: LoadingComponent ;
  @ViewChild(ErrorComponent) error: ErrorComponent ;
  @ViewChild(SuccessComponent) success: SuccessComponent ;
  Link = Links;
  registerForm: FormGroup;
  submitted = false;
  shipmentInfo:ShipmentInformation;
  selectedState:State;
  subscription: any;

  constructor(
    private el: ElementRef,
    public shared:SharingService,
    private userService:UserService,
    private formBuilder: FormBuilder) { }
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

    this.el.nativeElement.getElementsByClassName('shipmentEditContainer')[0].classList.add(this.shared.basketClass);

    this.registerForm = this.formBuilder.group({
      fullName: [''],
      email: [''],
      city: [''],
      state: [''],
      address: [''],
      workPlace: [''],
    });

    this.loading.show();
    this.userService.GetShipmentInformation().subscribe(result=>{
      this.loading.hide();
      this.shipmentInfo = result;
      this.registerForm = this.formBuilder.group({
        fullName: [this.shipmentInfo.fullName],
        email: [this.shipmentInfo.email],
        city: [this.shipmentInfo.city],
        state: [this.shipmentInfo.state.title],
        address: [this.shipmentInfo.address],
        workPlace: [this.shipmentInfo.workPlace],
      });
      this.selectedState = this.shipmentInfo.state;

    },
    error=>{
      this.loading.hide();
      this.error.show(error,3000,'/signin');
    })
  }
  SaveShipment(eventDate) {
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
      "state":this.selectedState.stateId,
      "address":this.formFields.address.value,
      "workPlace":this.formFields.workPlace.value,
    }

    this.userService.SetShipmentInformation(obj).subscribe(result => {
      this.success.show(result,1500)
      .then(()=>{
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
  goBack(){
    this.shared.basketClass = "myCfnAnimation-slideleft";
    this.shared.toggleMenu.address = false;
    this.shared.toggleMenu.preview = true;
  }
  goToNext(){
    this.shared.basketClass = "myCfnAnimation-slideright";
    this.shared.toggleMenu.address = false;
    this.shared.toggleMenu.payment = true;
  }
  toggleStates(eventDate){
    this.shared.states = true;
    eventDate.stopPropagation();
  }

  ngOnDestroy(){
    this.subscription.unsubscribe();
  }


}
