import {OrderDetail} from 'src/app/models/orderDetail.model'

export class Cart {
  orderId:number;
  itemId:number;
  price:number;
  discount:number;
  title:string;
  type:string;
  image:string;
  order_details:OrderDetail[];
}
