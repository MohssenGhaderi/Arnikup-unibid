import { Component, OnInit, Input } from '@angular/core';
import { ShipmentMethod } from 'src/app/models/shipmentMethod.model';

@Component({
  selector: 'app-shipment-method-item',
  templateUrl: './shipment-method-item.component.html',
  styleUrls: ['./shipment-method-item.component.css']
})
export class ShipmentMethodItemComponent implements OnInit {
  @Input() shipmentMethod:ShipmentMethod;

  constructor() { }

  ngOnInit() {
  }

}
