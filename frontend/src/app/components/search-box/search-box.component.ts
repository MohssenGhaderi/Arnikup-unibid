import { Component, OnInit, ViewChild, ElementRef, QueryList, ViewChildren} from '@angular/core';
import { SearchItems } from 'src/app/models/service/searchItems.model';
import { MainServices } from 'src/app/services/main.service';
import { SharingService } from 'src/app/services/sharing.service';
import { Links } from 'src/app/links.component';
import { Router } from '@angular/router';

@Component({
  selector: 'app-search-box',
  templateUrl: './search-box.component.html',
  styleUrls: ['./search-box.component.css']
})
export class SearchBoxComponent implements OnInit {
  searchItems: SearchItems;
  @ViewChild('searchToolbarSuggestion') searchToolbarSuggestion: ElementRef;
  @ViewChild('txtSearch') txtSearch: ElementRef;
  @ViewChildren('searchItemElements') searchItemElements:QueryList<ElementRef>;
  Link = Links;

  constructor(
    private service: MainServices,
    public shared: SharingService,
    private router:Router,
  ) { }

  ngOnInit() {
    this.service.GetSearchItems().subscribe(result => {
      this.searchItems = result;
      this.shared.search.max = this.searchItems.categories.length;
    },
    error => {
    });
  }

  searchBoxBehaviour(event) {
    if(this.shared.search.currentText==''){
      this.resetSearchItems();
      this.shared.search.max = this.searchItems.categories.length;
      this.searchToolbarSuggestion.nativeElement.classList.add('search-toolbar-suggestion-show');
    }else{
      this.searchToolbarSuggestion.nativeElement.classList.remove('search-toolbar-suggestion-show');
    }
  }

  searchItemClick(eventData) {
    this.txtSearch.nativeElement.value = eventData.target.textContent;
    this.shared.search.currentText = eventData.target.textContent;
    this.shared.search.currentId = this.searchItems.categories.find(item=>item.title.startsWith(this.shared.search.currentText)).categoryId;
    this.txtSearch.nativeElement.focus();
    this.searchToolbarSuggestion.nativeElement.classList.remove('search-toolbar-suggestion-show');
  }

  searchItemLostFocus(eventData){
    this.searchToolbarSuggestion.nativeElement.classList.remove('search-toolbar-suggestion-show');
  }

  onKeydown(eventData){

    switch(eventData.key){
      case "ArrowUp":{
        console.log('up');
        this.shared.search.dec();
        this.shared.search.setText(this.searchItems.categories[this.shared.search.currentIndex].title)
        this.shared.search.currentId = this.searchItems.categories[this.shared.search.currentIndex].categoryId;
        this.hoverSelected(this.shared.search.currentIndex);
        this.moveCursorToEnd(this.txtSearch.nativeElement);
        break;
      };
      case "Enter":{
        this.submitSearch();
        break;
      };
      case "ArrowDown":{
        this.shared.search.inc();
        this.shared.search.setText(this.searchItems.categories[this.shared.search.currentIndex].title)
        this.shared.search.currentId = this.searchItems.categories[this.shared.search.currentIndex].categoryId;
        this.hoverSelected(this.shared.search.currentIndex);
        break;
      };
    }

  }

  hoverSelected(index){
    this.searchItemElements.forEach(searchItem => {
      searchItem.nativeElement.classList.remove('search-toolbar-list-selected');
    });
    this.searchItemElements.toArray()[index].nativeElement.classList.add('search-toolbar-list-selected');
  }
  resetSearchItems(){
    this.shared.search.reset();

    this.searchItemElements.forEach(searchItem => {
      searchItem.nativeElement.classList.remove('search-toolbar-list-selected');
    });

  }

  onSearchChanges(value){
    this.shared.search.currentText = value;
  }

  moveCursorToEnd(el) {
    if (typeof el.selectionStart == "number") {
        el.selectionStart = el.selectionEnd = el.value.length;
    } else if (typeof el.createTextRange != "undefined") {
        el.focus();
        var range = el.createTextRange();
        range.collapse(false);
        range.select();
    }
  }

  submitSearch(){

    this.searchToolbarSuggestion.nativeElement.classList.remove('search-toolbar-suggestion-show');
    // this.shared.search.operate = true;
    this.router.navigate(['/search']);
    var selectedTitle = this.searchItems.categories.find(item=>item.categoryId==this.shared.search.currentId);
    if(selectedTitle && this.shared.search.currentText!=""){
      this.shared.search.keyword = this.shared.search.currentText.replace(selectedTitle.title,'');
      this.shared.emitSearchChanged({"text":this.shared.search.keyword.trim(),"categoryId":this.shared.search.currentId});

    }else{
      this.shared.search.currentText = this.txtSearch.nativeElement.value;
      this.shared.emitSearchChanged({"text":this.shared.search.currentText});
    }
  }

}
