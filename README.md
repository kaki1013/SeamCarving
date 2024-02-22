# SeamCarving  
 '최적화의 수학적 이론(Mathematical Optimization, 44141)' 과목을 수강하며 진행한 기말 프로젝트  
  
## 1. Seam Carving  
seam carving은 내용 인식 이미지 크기 조정(Content-Aware Image Resizing)을 위한 알고리즘 중 하나이다.  
이미지의 크기를 조절하면서, 이미지의 내용은 유지할 수 있도록 고안되었다.  
이 알고리즘은 이미지에 다수의 seam(중요도가 가장 낮은 경로)을 설정한 뒤, seam을 제거하거나 삽입함으로써 이미지의 크기를 줄이거나 확장한다.  

실제로, 이미지의 크기를 조절하는 다양한 방법이 있다.  
이미지의 전체적인 비율을 조절하는 scaling, 이미지의 특정 부분을 잘라내는 cropping,  
그리고 앞으로 살펴보게 될 seam carving이 바로 그것이다.  

  1) 원본 (Original)  
  ![1_0th_original](https://github.com/kaki1013/SeamCarving/assets/65400693/24ca59fc-407d-49a3-99a8-177eda00f2c3)  
  
  2) 비율 조정 (Scaling)  
  ![image](https://github.com/kaki1013/SeamCarving/assets/65400693/ee8622e8-42b7-4f1d-aa50-2930eed22296)  
  
  3) 자르기 (Cropping)  
  ![image](https://github.com/kaki1013/SeamCarving/assets/65400693/791ab6ee-a39f-417b-825d-adfc70d28cfe)  
  
  4) Seam Carving  
  ![image](https://github.com/kaki1013/SeamCarving/assets/65400693/b792a649-39f8-419c-8986-92fa4bde37e6)  
  ![1](https://github.com/kaki1013/SeamCarving/assets/65400693/24bb2e7b-e337-40bc-b6bf-5fb1ace02095)  

## 2. Files  
.  
├─demo  
│  ├─002_carved  
│  │  ├─1. basic  
│  │  ├─2. dominant  
│  │  └─3. preserve  
│  ├─002_red_line  
│  │  ├─1. basic  
│  │  ├─2. dominant  
│  │  └─3. preserve  
│  └─etc  
├── image  
│ └── 002.jpg  
├── Utils.py  
├── Seam_Carving.py  
└── main.py  
  
Utils.py : 구현을 위해 필요한 함수를 모아놓은 모듈  
Seam_Carving.py : Seam Carving 을 구현한 모듈 - 여러 옵션(ex. red_line : seam 시각화, is_preservation : 삭제가 불가능한 구역 지정 등) 적용 가능  
main.py : 옵션들을 변경하며 Seam Carving을 실행하는 main 파일  
image (directory) : 변경하고 싶은 이미지 파일(ex. 002.jpg)를 넣은 디렉토리  
demo (directory) : 002.jpg 파일에 여러 옵션을 적용하여 Seam Carving 을 수행한 파일들을 모아놓은 디렉토리  
