import { State } from './state.model'

export class ShipmentInformation {
  fullName : string;
  email : string;
  city:string;
  state:State;
  address:string;
  workPlace:string;
  states : State[];
}
