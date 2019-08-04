import { Pipe, PipeTransform } from '@angular/core';
import persianDate from 'persian-date';

@Pipe({
  name: 'persian'
})
export class PersianPipe implements PipeTransform {

  transform(value: any, args?: any): any {
    return new persianDate(new Date(value)).format(args);
  }

}
