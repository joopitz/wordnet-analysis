import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ImageInputParams } from '../models/image-input-params';
import { WordnetService } from '../services/wordnet.service';

@Component({
  selector: 'app-image-viewer',
  templateUrl: './image-viewer.component.html',
  styleUrls: ['./image-viewer.component.css']
})
export class ImageViewerComponent implements OnInit {

  imageParams!: ImageInputParams;
  imageSrc!: string;
  imageMaximized: boolean = false;

  constructor(
    private route: ActivatedRoute,
    private wordnetService: WordnetService,
    private cd: ChangeDetectorRef,
    ) {


  }

  addSynonyms(count: number): void {

    if (this.imageParams?.synonymCount) {
      this.imageParams.synonymCount += count;
      if (this.imageParams.synonymCount < 1) {
        this.imageParams.synonymCount = 1
      }
      this.loadImage();
    }
    
  }

  addMaxLeafNodes(count: number): void {
    if (this.imageParams?.maxLeafNodes) {
      this.imageParams.maxLeafNodes += count;
      if (this.imageParams.maxLeafNodes < 1) {
        this.imageParams.maxLeafNodes = 1
      }
      this.loadImage();
    }
    
  }

  addLevel(count: number): void {
    if (this.imageParams?.level) {
      this.imageParams.level += count;
      if (this.imageParams.level < 1) {
        this.imageParams.level = 1
      }
      this.loadImage();
    }
    
  }

  private loadImage(): void {
    if (this.imageParams && this.imageParams.synsetId) {
      this.imageParams.fileName = `hierarchy_partwhole${Date.now()}${['de'].join('_')}_${this.imageParams.level}_${this.imageParams.maxLeafNodes}${this.imageParams.synonymCount}`;                    
      this.wordnetService.getImage(this.imageParams).subscribe((imageStr: string) => {
        this.imageSrc = imageStr;
        this.cd.detectChanges();
      });
     
    }
    
  }
  
  ngOnInit(): void {

    this.route.queryParams.subscribe(params => {
      
      this.imageParams = {
        fileName: params["fileName"] as string,
        synsetId: params["synsetId"] as string,
        level: params["level"] ? parseInt(params["level"]): 2,
        maxLeafNodes: params["maxLeafNodes"] ? parseInt(params["maxLeafNodes"]): 5,
        synonymCount: params["synonymCount"] ? parseInt(params["synonymCount"]): 1,
        filterLangs: params["filterLangs"] ? params["filterLangs"] as string: 'de',
        partWhole: params["partWhole"] ? params["partWhole"] as string: "True",
        hierarchy: params["hierarchy"] ? params["hierarchy"] as string: "True"
      };
      this.loadImage();
      
      
    });

  }

}
