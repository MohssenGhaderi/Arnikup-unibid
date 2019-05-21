import { Directive, HostListener, ElementRef } from '@angular/core';

@Directive({
  selector: '[appVerificationInputKeyup]'
})
export class VerificationInputKeyupDirective {

  constructor(private elRef: ElementRef) { }

  @HostListener('keyup') keyUp() {
    const nextSibling = this.elRef.nativeElement.nextSibling;
    if(nextSibling) {
      if (this.elRef.nativeElement.textContent !== '') {
        nextSibling.focus();
      }
    }
    else {
      this.elRef.nativeElement.blur();
    }
  }

  @HostListener('focus') focus() {
    this.elRef.nativeElement.textContent = '';
  }

}
